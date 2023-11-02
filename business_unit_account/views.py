from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff,Collage, Trainingprogram
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages
from django.utils import timezone



@login_required
def business_unit_home (request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    staff = collage.nostaff 
    faculty = collage.nofaculty
    emp = staff + faculty
    count = len(collage.departments)

    context = {'user': user , 'collage':collage , "emp":emp , 'department':count }

    return render(request, 'bu/Home.html', context)

@login_required
def profile_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 

    context = {'user': user , 'collagename':collagename }
    return render(request, 'bu/profile.html', context)

def view_file(request, user_id):
    # Retrieve the user based on the user_id
    user = get_object_or_404(FacultyStaff, pk=user_id)
    # Check if the user has a CV
    if user.cv:
        cv = user.cv  # Assuming that the CV field contains the binary CV data
        response = FileResponse(cv, content_type='application/pdf')  # Change content type accordingly
        response['Content-Disposition'] = f'inline; filename="{user.first_name}-CV.pdf"'  # Provide a filename
        return response

    # If the user doesn't have a CV or the CV is not found, return a 404 error
    raise Http404("CV not found")

@login_required
def facultylist_view (request):
    user = request.user
    faculty = FacultyStaff.objects.filter(collageid=user.collageid.collageid)
    
    collage = Collage.objects.get(collageid=user.collageid.collageid)
    departments = collage.departments
    context = {
        'faculty': faculty,
        'departments': departments,
    }
    return render(request, 'bu/faculty-list.html', context)

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
                # return redirect('business_unit_account:profile')
            
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
                        # return redirect('business_unit_account:edit-profile')
                   
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
                        return redirect('business_unit_account:edit-profile')

    return render(request, 'bu/edit-profile.html', {'form': form ,'form2':form2, 'user' : user , 'success':success , 'form2updated':form2updated })



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

    return redirect('business_unit_account:edit-profile')


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

    return redirect('business_unit_account:edit-profile')

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
            success = True

    return render(request, 'bu/change-password.html', {'user': user, 'form': form , 'success':success})

@login_required
def facultyinfo_view(request,faculty_id):
    faculty_member = get_object_or_404(FacultyStaff, id=faculty_id)
    collage_id = faculty_member.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    return render(request, 'bu/faculty-view.html', {'faculty_member': faculty_member , 'collagename': collagename})

@login_required
def traningprogram_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    programs = Trainingprogram.objects.filter(collageid=collage_id)
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
    
    for program in programs:
        instructor_id = program.instructorid
        try:
            faculty_staff = FacultyStaff.objects.get(id=instructor_id)
            program.instructor_first_name = faculty_staff.first_name
            program.instructor_last_name = faculty_staff.last_name
        except FacultyStaff.DoesNotExist:
            program.instructor_first_name = ""
            program.instructor_last_name = ""

    if request.method == 'POST':
        programtype = request.POST.get('reqType')
        topic = request.POST.get('topic')
        Domain = request.POST.get('domain')
        price = request.POST.get('price')
        capacity = request.POST.get('numoftrainee')
        instructor_id = request.POST.get('instructor')
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        start_time = request.POST.get('starttime')
        end_time = request.POST.get('endtime')
        subject = request.POST.get('subject')
        attachment = request.FILES.get('attachment')
        
    
        new_program = Trainingprogram(
            programtype=programtype,
            instructorid=instructor_id,
            capacity=capacity,
            subject=subject,
            topic=topic,
            program_domain=Domain,
            totalcost=price,
            startdate=start_date,
            enddate=end_date,
            starttime=start_time,
            endtime=end_time,
            attachment=attachment,
            collageid=collage_id,
            dataoffacultyproposal = timezone.now().date()
        )
        new_program.save()

    return render(request, 'bu/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain })


@login_required
def delete_course(request, value_to_delete):
    # user = request.user
    program = Trainingprogram.objects.get(programid=value_to_delete)

    if program:
        program.delete()
    else:
        messages.error(request, 'No researchinterest values to delete.')

    return redirect('business_unit_account:traning-program')