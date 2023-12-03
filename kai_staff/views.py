from datetime import timezone
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.forms import updateKai,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages
from app.models import FacultyStaff,Collage, Trainingprogram,Register,Trainees,StatusDateCheck
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.http import FileResponse
import mimetypes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import base64
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from django.views.decorators.http import require_POST

@login_required
def kaistaff_home (request):
    user = request.user
    return render(request, 'kai_staff/Home.html', {'user': user })
      
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'kai_staff/profile.html' ,{'user': user}) 

@login_required
def editprofile_view(request):
    user = request.user
    form = updateKai(instance=user)
 
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateKai(request.POST, instance=user)   
            if form.is_valid():          
                form.save()
                return redirect('kai_staff:profile')
            
    return render(request, 'kai_staff/edit-profile.html', {'form': form , 'user' : user})

@login_required
def changepassword_view(request):
    user = request.user
    form = ChangePasswordForm(user)
    
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('kai_staff:profile')

    return render(request, 'kai_staff/change-password.html', {'user': user, 'form': form})

@login_required
def traningprogram_view(request):
    user = request.user
    programs = StatusDateCheck.objects.filter()
   
    for program in programs:
        Collage_id = program.training_program.collageid
        collage = Collage.objects.get(collageid = Collage_id)
        collagename = collage.name
        program.collagename = collagename
        
    return render(request, 'kai_staff/TraningPrograms.html', {'user': user , 'programs':programs})


@login_required
def view_certifications(request, register_id):
    document = get_object_or_404(Register, pk=register_id)

    if document.certifications:
        certifications_name = document.certifications_ext
        file_extension = certifications_name.split('.')[-1] if '.' in certifications_name else ''
        content_type, _ = mimetypes.guess_type(certifications_name)
       
        decoded_data = base64.b64decode(document.certifications)

        if content_type:
            response = HttpResponse( decoded_data, content_type=content_type)
        else:
            if file_extension.lower() == 'pdf':
                response = HttpResponse(decoded_data, content_type='application/pdf')
            elif file_extension.lower() == 'pptx':
                response = HttpResponse(decoded_data, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            elif file_extension.lower() in ['doc', 'docx']:
                response = HttpResponse(decoded_data, content_type='application/msword')
            else:
                response = HttpResponse(decoded_data, content_type='application/octet-stream')

        response['Content-Disposition'] = f'inline; filename="{certifications_name}"'
        return response

    raise Http404("Document not found")


@login_required
def program_view(request , program_id):
    program = get_object_or_404(Trainingprogram, programid=program_id)
    instructors = program.instructorid
    
    instructors_id = program.instructorid
    instructor_names = []
    for instructors in instructors_id:
        try:
            faculty_staff = FacultyStaff.objects.get(id=instructors)
            name = [faculty_staff.first_name +' '+faculty_staff.last_name , faculty_staff.id , faculty_staff.major , faculty_staff.email , faculty_staff.iban]
            instructor_names.append(name)
        except FacultyStaff.DoesNotExist:
            instructor_names.append("")
    program.instructor_names = instructor_names


    Registertraniees = Register.objects.filter(programid=program_id ,haspaid = True )
    traniees_names = []
    for register in Registertraniees:
        try:
            traniee_info = Trainees.objects.get(id=register.id.id)
            name = [traniee_info.fullnamearabic , register.haspaid , register.id.id , register.certifications , register.registerid]
            traniees_names.append(name)
        except Trainees.DoesNotExist:
            traniees_names.append("")

    program.traniees_names = traniees_names
    return render(request, 'kai_staff/TraningProgram-view.html', {'program': program})

  
@login_required
def save_certifications(request, program_id, trainee_id):
    if request.method == 'POST' and request.FILES.get('attachment'):
        try:
            trainee = Register.objects.get(id=trainee_id, programid=program_id)
            uploaded_file = request.FILES['attachment']
            attachment_name = request.FILES['attachment'].name
            
            binary_data = base64.b64encode(uploaded_file.read()).decode('utf-8')  
            # print(binary_data)
            trainee.certifications = binary_data
            trainee.certifications_ext = attachment_name
            trainee.save()

            return JsonResponse({ 'success_message': 'تم الرفع بنجاح' })
            
        except Register.DoesNotExist:
            return JsonResponse({'error_message': 'Register not found'})
        
        except Exception as e:
            return JsonResponse({'error_message': f'An error occurred: {e}'})

    # Default response if the form submission fails
    return JsonResponse({'error_message': 'Form submission failed'})

@login_required
def delete_certifications(request, register_id):
        try:
            trainee = Register.objects.get(registerid=register_id)
            
            # delete the certifications 
            trainee.certifications = None
            trainee.certifications_ext = None
            trainee.save()
            return JsonResponse({'success_message': 'certificate deleted'})

        except Register.DoesNotExist:
            print('here2')
            return JsonResponse({'error_message': 'Register not found'})

        except Exception as e:
            print('here3')
            return JsonResponse({'error_message': f'An error occurred: {e}'})


@login_required
def accept_program(request, id):
    program = Trainingprogram.objects.get(programid=id)
   
    # Change status of the current IdStatusDate object
    kaipercentage = request.POST.get('kaipercentage')
    program.kaipercentage = float(kaipercentage)
    program.status = "تم قبول الطلب من قبل المعهد"
    program.iskaiaccepted=True
    program.dataofkaiacceptance=timezone.now().date()
    program.save()

    # Check if all IdStatusDate objects associated with the same training program have been accepted
    
    # If all have been accepted, update StatusDateCheck objects
    status_date_checks = StatusDateCheck.objects.filter(training_program=id)
    status_date_checks.filter(status="تم قبول الطلب من قبل المعهد").update(indicator='T' , date=timezone.now().date())
    status_date_checks.filter(status="انتظار قبول المعهد").update(indicator='T')
    status_date_checks.filter(status="تم نشر البرنامج").update(indicator='C')
    return redirect('kai_staff:program_view' , program_id = program.programid)


@login_required
@require_POST
def rejecte_program(request, id):
    rejection_reason = request.POST.get('rejectionReason')
    program = get_object_or_404(Trainingprogram, programid=id)
    program.status ="تم رفض الطلب من قبل المعهد"
    program.rejectionresons=rejection_reason
    program.iskaiaccepted=False
    program.dataofkairejection=datetime.now().date()
    program.save()
    return redirect('kai_staff:traning-program')


