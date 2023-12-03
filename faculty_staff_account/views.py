from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff,Collage, Trainingprogram,Register,Trainees,IdStatusDate, StatusDateCheck 
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404, HttpResponse
import mimetypes
from django.views.decorators.http import require_POST

@login_required
def faculty_staff_home (request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)

    context = {'user': user , 'collage':collage , }

    return render(request, 'faculty_staff/Home.html', context)
     
@login_required
def profile_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    context = {'user': user , 'collagename':collagename }
    return render(request, 'faculty_staff/profile.html' ,context) 

@login_required
def emptypage_view (request):
     return render(request, 'faculty_staff/empty-page.html') 

def view_file(request, user_id):
    user = get_object_or_404(FacultyStaff, pk=user_id)
    if user.cv:
        cv = user.cv  
        response = FileResponse(cv, content_type='application/pdf')  
        response['Content-Disposition'] = f'inline; filename="{user.first_name}-CV.pdf"'  
        return response
    raise Http404("CV not found")

@login_required
def editprofile_view(request):
    user = request.user
    form = updateFASform(instance=user)
    form2 = previousworkform()
    success = False
    form2updated = False
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateFASform(request.POST, request.FILES, instance=user)   
            if form.is_valid():  
                cv_file = form.cleaned_data['cv']
                if cv_file is not None:
                    user.cv = cv_file.file.read()              
                
                form.save()
                success = True
                return redirect('faculty_staff_account:profile')
            
        elif form_type == 'form2':  
            form2 = previousworkform(request.POST)  
            if form2.is_valid():
                previouswork = form2.cleaned_data['previouswork']
                researchinterest = form2.cleaned_data['researchinterest']

                if previouswork:
                    previous_work = user.previouswork or []
                    for item in previouswork:
                        pw = item
                    if len(pw) < 5 :
                         messages.error(request,'يجب أن يكون  5 أحرف على الأقل.')
                    elif pw.isdigit():
                         messages.error(request,'يجب ألا يحتوي على أرقام فقط.')
                    elif pw[0].isdigit():
                         messages.error(request,'الحرف الأول لا يمكن ان يكون رقم.')
                    else: 
                        previous_work.extend(previouswork)
                        user.previouswork = previous_work
                        user.save()
                        form2updated = True
                        return redirect('faculty_staff_account:edit-profile')
                   
                if researchinterest:
                    research_interest = user.researchinterest or []
                    for item in researchinterest:
                        ri = item
                    if len(ri) < 5:
                       messages.error(request,'يجب أن يكون  5 أحرف على الأقل.')
                    elif ri.isdigit():
                        messages.error(request,'يجب ألا يحتوي على أرقام فقط.')
                    elif ri[0].isdigit():
                        messages.error(request,'الحرف الأول لا يمكن ان يكون رقم.')
                    else:
                        research_interest.extend(researchinterest)
                        user.researchinterest = research_interest
                        user.save()
                        return redirect('faculty_staff_account:edit-profile')

    return render(request, 'faculty_staff/edit-profile.html', {'form': form ,'form2':form2, 'user' : user , 'success':success , 'form2updated':form2updated })


@login_required
def delete_previouswork(request, value_to_delete):
    user = request.user

    if user.previouswork:
        if value_to_delete in user.previouswork:
            user.previouswork.remove(value_to_delete)
            user.save()
        else:
            messages.error(request, 'Value not found in previouswork.')
    else:
        messages.error(request, 'No previouswork values to delete.')

    return redirect('faculty_staff_account:edit-profile')

@login_required
def delete_researchinterest(request, value_to_delete):
    user = request.user

    if user.researchinterest:
        if value_to_delete in user.researchinterest:
            user.researchinterest.remove(value_to_delete)
            user.save()
        else:
            messages.error(request, 'Value not found in previouswork.')
    else:
        messages.error(request, 'No researchinterest values to delete.')

    return redirect('faculty_staff_account:edit-profile')

@login_required
def changepassword_view(request):
    user = request.user
    form = ChangePasswordForm(user)
    success = False
    
    if request.method == 'POST':
        print('here1')
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            # messages(request, 'Password changed successfully.') 
            return redirect('faculty_staff_account:profile')

    return render(request, 'faculty_staff/change-password.html', {'user': user, 'form': form , 'success':success })

@login_required
def delete_course(request, value_to_delete):
    program = Trainingprogram.objects.get(programid=value_to_delete)
    if program:
        program.delete()
    else:
        messages.error(request, 'No values to delete.')

    return redirect('faculty_staff_account:traning-program')

@login_required
def traningprogram_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    programs = Trainingprogram.objects.filter(collageid=collage_id)
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
    
        
    bu_programs = Trainingprogram.objects.filter(collageid=collage_id,instructorid__contains=[user.id]).exclude(programleader=user.id)
    print(bu_programs)
    faculty_or_staff_programs = Trainingprogram.objects.filter(collageid=collage_id, initiatedby='FacultyOrStaff' , programleader=user.id)
    opent_to_all_programs = Trainingprogram.objects.filter(collageid=collage_id,appourtunityopentoall=True,status='فتح الفرصة للجميع').exclude(programleader=user.id)
    opent_to_all_programs_list = list(opent_to_all_programs)
    bu_programs_list = list(bu_programs)
    combined_programs = opent_to_all_programs_list + bu_programs_list


    if request.method == 'POST':
        programtype = request.POST.get('reqType')
        topic = request.POST.get('topic')
        Domain = request.POST.get('domain')
        price = request.POST.get('price')
        priceType = request.POST.get('priceType')
        capacity = request.POST.get('numoftrainee')
        instructors_id = request.POST.getlist('instructor')
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        start_time = request.POST.get('starttime')
        end_time = request.POST.get('endtime')
        Descriptionofrequirements = request.POST.get('subject')
        num_ofinstructors = request.POST.get('num_ofinstructors')
        pricefortrainee  = request.POST.get('pricefortrainee')
        isOnline = request.POST.get('isonline')

        if isOnline == "online" :
            isOnline = True
        else:
            isOnline = False
        
        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = None
            attachment_name = ''
        
        if programtype == 'other':
            programtype = request.POST.get('otherText')
        
        if Domain == 'اخرى':
            Domain = request.POST.get('otherdomain')

   
        new_program = Trainingprogram(
            isonline = isOnline,
            programleader = user.id,
            programtype=programtype,
            instructorid=instructors_id,
            num_ofinstructors=num_ofinstructors,
            capacity=capacity,
            Descriptionofrequirements=Descriptionofrequirements,
            topic=topic,
            program_domain=Domain,
            cost=price,
            costtype=priceType,
            startdate=start_date,
            enddate=end_date,
            starttime=start_time,
            endtime=end_time,
            attachment=attachment,
            totalcost = pricefortrainee,
            attachment_name=attachment_name,
            collageid=collage_id,
            # isfacultyfound= True,
            iskaiaccepted=False,
            isreleased_field=False,
            isbuaccepted=False,
            initiatedby='FacultyOrStaff',
            status="في انتظار قبول وحدة الأعمال",
            dataoffacultyproposal = timezone.now().date()
        )
        new_program.save()

        tempStatus="تم ارسال الطلب إلى وحدة الاعمال"
        tempStatus2="انتظار قبول الطلب من قبل وحدة الاعمال"
        tempStatus3= "تم قبول الطلب من قبل وحدة الاعمال"

        new_StatusDateCheck =StatusDateCheck(
                status="إنشاء الطلب من قبل المدرب",
                date=timezone.now().date(),
                indicator='T',
                training_program=new_program)
        new_StatusDateCheck.save()

        new_StatusDateCheck2 =StatusDateCheck(
                status=tempStatus,
                date=timezone.now().date(),
                indicator='T',
                training_program=new_program)
        new_StatusDateCheck2.save()

        new_StatusDateCheck3 =StatusDateCheck(
                status=tempStatus2,
                date=None,
                indicator='C',
                training_program=new_program)
        new_StatusDateCheck3.save()
        
        new_StatusDateCheck4 =StatusDateCheck(
                status=tempStatus3,
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck4.save()

        new_StatusDateCheck5 =StatusDateCheck(
                status="تم ارسال الطلب إلى المعهد",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck5.save()

        new_StatusDateCheck61 =StatusDateCheck(
                status="انتظار قبول المعهد",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck61.save()

        new_StatusDateCheck6 =StatusDateCheck(
                status="تم قبول الطلب من قبل المعهد",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck6.save()

        new_StatusDateCheck7 =StatusDateCheck(
                status="تم نشر البرنامج ",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck7.save()

        new_StatusDateCheck10 =StatusDateCheck(
                status="انتهى تسجيل المتدربين",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck10.save()

        new_StatusDateCheck8 =StatusDateCheck(
                status="بدأ البرنامج",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck8.save()

        new_StatusDateCheck9 =StatusDateCheck(
                status="إنتهاء البرنامج",
                date=None,
                indicator='W',
                training_program=new_program)
        new_StatusDateCheck9.save()

        new_StatusDateCheck10 =StatusDateCheck(
                        status="فتح التقديم لتقديم البرنامج لأعضاء هيئة التدريس ",
                        date=None,
                        indicator='W',
                        training_program=new_program)
        new_StatusDateCheck10.save()

        new_IdStatusDate = IdStatusDate(
                instructor=user,
                status="تم قبول الطلب من قبل المدرب",
                date=timezone.now().date(),
                training_program=new_program)
        new_IdStatusDate.save()

        return redirect('faculty_staff_account:traning-program')

    return render(request, 'faculty_staff/TraningPrograms.html', {'user': user ,'combined_programs':combined_programs, 'programs':programs,'faculty':faculty, 'domain':domain , 'bu_programs':bu_programs ,'faculty_or_staff_programs':faculty_or_staff_programs ,'opent_to_all_programs':opent_to_all_programs  })

@login_required
def program_view(request , program_id):
    program = get_object_or_404(Trainingprogram, programid=program_id)
    instructors = program.instructorid
    user = request.user
    instructors_id = program.instructorid
    instructor_names = []
    for instructors in instructors_id:
        try:
            faculty_staff = FacultyStaff.objects.get(id=instructors)
            name = [faculty_staff.first_name +' '+faculty_staff.last_name , faculty_staff.id , faculty_staff.major , faculty_staff.email ]
            instructor_names.append(name)
        except FacultyStaff.DoesNotExist:
            instructor_names.append("")
    program.instructor_names = instructor_names

    if program.programleader:
        Requestername = FacultyStaff.objects.get(id = program.programleader)
        name = Requestername.first_name +' '+Requestername.last_name
        program.Requestername = name

    id_status_dates = IdStatusDate.objects.filter(training_program=program )
    programflow = StatusDateCheck.objects.filter(training_program=program)
    applicationidcount = IdStatusDate.objects.filter(status='participationRequest', instructor =user.id).count()
    
    if applicationidcount:
        isfacultyinarray = False
        print('here1')
    else:
        isfacultyinarray = True
        print('here2')
    
  

    Registertraniees = Register.objects.filter(programid=program_id)
    traniees_names = []
    for register in Registertraniees:
        try:
            traniee_info = Trainees.objects.get(id=register.id.id)
            name = [traniee_info.fullnamearabic , register.hasattended , register.id.id , register.registerid, traniee_info.email, traniee_info.phonenumber]
            traniees_names.append(name)
        except Trainees.DoesNotExist:
            traniees_names.append("")
    program.traniees_names = traniees_names

    return render(request, 'faculty_staff/TraningProgram-view.html', {'userid': user.id ,'program': program , 'id_status_dates': id_status_dates ,'programflow':programflow ,'isfacultyinarray': isfacultyinarray , 'applicationidcount':applicationidcount})


@login_required
def hasattend(request, register_id):
        print('here1')
        try:
            trainee = Register.objects.get(registerid=register_id) 
            if trainee.hasattended:
                trainee.hasattended = False
            else:
                trainee.hasattended = True
            trainee.save()
            return JsonResponse({'success_message': trainee.hasattended})

        except Register.DoesNotExist:
            print('here2')
            return JsonResponse({'error_message': 'Register not found'})

        except Exception as e:
            print('here3')
            return JsonResponse({'error_message': f'An error occurred: {e}'})


def view_programfile(request, program_id):
    document = get_object_or_404(Trainingprogram, pk=program_id)
    
    if document.attachment:
        attachment_name = document.attachment_name
        file_extension = attachment_name.split('.')[-1] if '.' in attachment_name else ''
        content_type, _ = mimetypes.guess_type(attachment_name)
        
        if content_type:
            response = HttpResponse(document.attachment, content_type=content_type)
        else:
            if file_extension.lower() == 'pdf':
                response = HttpResponse(document.attachment, content_type='application/pdf')
            elif file_extension.lower() == 'pptx':
                response = HttpResponse(document.attachment, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            elif file_extension.lower() in ['doc', 'docx']:
                response = HttpResponse(document.attachment, content_type='application/msword')
            else:
                response = HttpResponse(document.attachment, content_type='application/octet-stream')

        response['Content-Disposition'] = f'inline; filename="{attachment_name}"'
        return response

    raise Http404("Document not found")


@login_required
def edit_program(request, value_to_edit):
    editprogram = Trainingprogram.objects.get(programid=value_to_edit)
    user = request.user
    collage_id = user.collageid.collageid
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
    id_status_dates = IdStatusDate.objects.filter(training_program=editprogram)
    programflow = StatusDateCheck.objects.filter(training_program=editprogram)
   
    if request.method == 'POST':
        programtype = request.POST.get('reqType')
        topic = request.POST.get('topic')
        Domain = request.POST.get('domain')
        price = request.POST.get('price')
        priceType = request.POST.get('priceType')
        capacity = request.POST.get('numoftrainee')
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        start_time = request.POST.get('starttime')
        end_time = request.POST.get('endtime')
        Descriptionofrequirements = request.POST.get('subject')
        num_ofinstructors = request.POST.get('num_ofinstructors')
        pricefortrainee  = request.POST.get('pricefortrainee')
        isOnline = request.POST.get('isonline')

        if isOnline == "online" :
            isOnline = True
        else:
            isOnline = False

        if not programtype:
            programtype = editprogram.programtype

        if not priceType:
            priceType = editprogram.costtype
        

        if not Domain:
            Domain = editprogram.program_domain

        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = editprogram.attachment
            attachment_name = editprogram.attachment_name
        
        if programtype == 'other':
            programtype = request.POST.get('otherText')
        
        if Domain == 'اخرى':
            Domain = request.POST.get('otherdomain')

        
        editprogram.isonline = isOnline
        editprogram.programtype = programtype
        editprogram.num_ofinstructors=num_ofinstructors
        editprogram.capacity=capacity
        editprogram.Descriptionofrequirements=Descriptionofrequirements
        editprogram.topic=topic
        editprogram.program_domain=Domain
        editprogram.cost=price
        editprogram.costtype=priceType
        editprogram.startdate=start_date
        editprogram.enddate=end_date
        editprogram.starttime=start_time
        editprogram.endtime=end_time
        editprogram.attachment=attachment
        editprogram.attachment_name=attachment_name
        editprogram.totalcost = pricefortrainee

        editprogram.save()
        return redirect('faculty_staff_account:program_view', program_id = editprogram.programid )

    return render(request, 'faculty_staff/TraningProgram-edit.html', {'program':editprogram ,'faculty':faculty , 'domain':domain ,'id_status_dates':id_status_dates ,'programflow':programflow })


def get_programs_initiated_by_bu(user):
    collage_id = user.collageid.collageid
    programs = Trainingprogram.objects.filter(collageid=collage_id, initiatedby='bu')
    for program in programs:
        instructor_id = program.instructorid
        try:
            faculty_staff = FacultyStaff.objects.get(id=instructor_id)
            program.instructor_first_name = faculty_staff.first_name
            program.instructor_last_name = faculty_staff.last_name
        except FacultyStaff.DoesNotExist:
            program.instructor_first_name = ""
            program.instructor_last_name = ""
    return programs


def update_status(request, program_id):

    print("enterid update status successfully")
    program = get_object_or_404(Trainingprogram, programid=program_id)
    print(program)
    user = request.user
    collage_id = user.collageid.collageid
    programs = Trainingprogram.objects.filter(collageid=collage_id)
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
 
    if request.method == "POST":
        status_value = request.POST.get('update_status')

        if status_value == "understudy":
            program.status = "تحت الدراسة من قبل المدرب"
        elif status_value == "accept":
            program.status = "تم قبول الطلب من قبل المتدرب"
        elif status_value == "reject":
            program.status = "تم الرفض من قبل المتدرب"
        
        program.save()
        print(program.status)
        for program in programs:
            instructor_id = program.instructorid
            try:
                faculty_staff = FacultyStaff.objects.get(id=instructor_id)
                program.instructor_first_name = faculty_staff.first_name
                program.instructor_last_name = faculty_staff.last_name
            except FacultyStaff.DoesNotExist:
                program.instructor_first_name = ""
                program.instructor_last_name = ""
    

    return render(request, 'faculty_staff/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain })


@login_required
@require_POST
def accept_program(request, id):
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    training_program = id_status_date.training_program

    # Change status of the current IdStatusDate object
    id_status_date.status = "تم قبول الطلب من قبل المدرب"
    id_status_date.date = timezone.now().date()
    id_status_date.save()

    # Check if all IdStatusDate objects associated with the same training program have been accepted
    id_status_dates2 = IdStatusDate.objects.filter(training_program=training_program)
    total_count = id_status_dates2.count()
    accepted_count = id_status_dates2.filter(status="تم قبول الطلب من قبل المدرب").count()

    if training_program.num_ofinstructors == len(training_program.instructorid):
        # If the number of instructors equals the total numbers of values in instructorid

        # Ensure all the ids in instructorid either not found in status_date_checks or status="تم قبول الطلب من قبل المدرب"
        status_date_checks = StatusDateCheck.objects.filter(training_program=training_program)
        for instructor_id in training_program.instructorid:
            if not id_status_dates2.filter(instructor=instructor_id).exists() or id_status_dates2.filter(status="تم قبول الطلب من قبل المدرب", instructor=instructor_id).exists():
                continue
            else:
                break
        else:
            # If the above condition is met, update the training program status
            if training_program.num_ofinstructors == 1 or training_program.num_ofinstructors =='1':
                training_program.status = "تم قبول الطلب من قبل المدرب"
                status_date_checks.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
            else:
                training_program.status = "تم قبول الطلب من قبل جميع المدربين"
                status_date_checks.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T' , date=timezone.now().date())
            
            status_date_checks.filter(status="تم ارسال الطلب إلى المعهد").update(indicator='C')
            training_program.save()

    return redirect('faculty_staff_account:program_view' , program_id = training_program.programid )


@login_required
@require_POST
def apply_for_traningprogram(request, id):
    user = request.user
    training_program = get_object_or_404(Trainingprogram, programid=id)

    IdStatusDate.objects.create(
                instructor_id=user.id,
                status="participationRequest",
                date=timezone.now().date(),
                training_program=training_program)
    
    return redirect('faculty_staff_account:traning-program')

  
@login_required
@require_POST
def reject_program(request, id):
    rejection_reason = request.POST.get('rejectionReason')
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    training_program = id_status_date.training_program
    print("instructors ids prior are :", training_program.instructorid )

    # Change status of the current IdStatusDate object
    id_status_date.status = "تم رفض الطلب من قبل المدرب"
    id_status_date.date = timezone.now().date()
    id_status_date.rejectionresons= rejection_reason
    id_status_date.save()

    # Remove instructor's id from the instructorid array in the associated TrainingProgram object
    instructor_id = id_status_date.instructor_id
    training_program.instructorid = [id for id in training_program.instructorid if id != instructor_id]
    training_program.save()

    return redirect('faculty_staff_account:traning-program')
