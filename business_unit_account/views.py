import base64
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff,Collage, Trainingprogram,Register,Trainees,IdStatusDate, StatusDateCheck, Files, Project, StatusDateCheckProject
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse , JsonResponse , HttpResponseBadRequest
import mimetypes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

################### communication ###################

@login_required
def callsDashboard(request):
    return render(request, 'bu/calls-dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    return render(request, 'bu/videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required
def joinroom(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/business-unit-account/business-unit-home/videocall?roomID=" + roomID)
    return render(request, 'bu/joinroom.html')

@login_required
def groupchat_view(request, program_id):
    
    project = Project.objects.get(programid=program_id)
    if project.chatgroup_id:
         chatid = project.chatgroup_id
         access_key = project.chat_access_key
         context = {'chatgroup_id':chatid , 'program_id':program_id ,'username': request.user.username , 'pass' :request.user.id , 'access_key':access_key }
         return render(request, 'bu/groupchat.html' , context)
    else:
       chat_credentials = creategroupchat(request , project )
       project.chatgroup_id = chat_credentials['chatid']
       project.chat_access_key = chat_credentials['access_key']
       project.save()
       context = {'chatgroup_id':project.chatgroup_id , 'program_id':program_id ,'username': request.user.username , 'pass' :request.user.id , 'access_key': project.chat_access_key }
       return render(request, 'bu/groupchat.html' , context)

@login_required
def creategroupchat(request , project):
    usernamess = []
    for teamMemberID in project.Teamid:
        user = FacultyStaff.objects.get(id=teamMemberID)
        usernamess.append(user.username)

    print(usernamess)
    print('------------------')
    url = "https://api.chatengine.io/chats/"
    payload = {
        "title": project.Name,
        "is_direct_chat": False,
        "usernames":usernamess
    }
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name':  request.user.username,
        'User-Secret': str(request.user.id),
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print('------------------')
    # print(response.text)
    # print(response.json())
    responseINjson = response.json()
    access_key = responseINjson['access_key']
    chatid = responseINjson['id']
    chat_credentials = {'access_key':access_key , 'chatid':chatid}
    print('chat_credentials' ,chat_credentials)
    print('response.status_code' ,response.status_code)
    return chat_credentials 

@login_required
def chat(request):
    username = request.user.username
    secret = request.user.id
    users = filteredUsers(request)
    return render(request, 'bu/chat.html' , {'username':username , 'secret': secret ,'users':users})

@login_required
def myChat(request):
    url = "https://api.chatengine.io/chats/"

    payload = {}
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name': request.user.username,
        'User-Secret': str(request.user.id),
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status() 

        users = response.json()
        my_users = []

        for user_data in users:
            people_data = user_data.get('people', [])
            for person_data in people_data:
                person = person_data.get('person', {})
                username = person.get('username', '')
                my_users.append({'username': username})

        return my_users

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
    
@login_required
def filteredUsers(request):
    mychat = myChat(request)
  
    print("my_fi")
    # print(mychat)
    url = "https://api.chatengine.io/users/"
    payload = {}
    headers = {'PRIVATE-KEY': '499cc31a-d338-455c-8e1c-7ea6e54afc38'}

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()  

        users = response.json()
        matching_users = []
        # print('users' , users)
        for checkuser in users:
            if checkuser['username'] not in [entry['username'] for entry in mychat]:
                try:
                    newuser = FacultyStaff.objects.get(username=checkuser['username'])
                except FacultyStaff.DoesNotExist:
                    newuser = None 

                if newuser: 
                    collageidRequest = request.user.collageid.collageid
                    if newuser.id != request.user.id:
                        if newuser.collageid.collageid == collageidRequest or newuser.is_buhead:
                            matching_users.append({'username': checkuser.get('username'), 'secret': checkuser.get('secret'),'first_name':checkuser.get('first_name'),'last_name':checkuser.get('last_name')})
                else:
                    matching_users.append({'username': checkuser.get('username'), 'secret': checkuser.get('secret'),'first_name':checkuser.get('first_name'),'last_name':checkuser.get('last_name')})

        # print("Matching users:", matching_users)
        return matching_users

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []
    
@login_required
def createDirect(request,direct_username):
  
    url = "https://api.chatengine.io/chats/"
    payload = {
        "title": direct_username,
        "is_direct_chat": False,
        "usernames":direct_username    
    }
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name':  request.user.username,
        'User-Secret': str(request.user.id),
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    responseINjson = response.json()
    users = filteredUsers(request)
    context = {'username': request.user.username , 'secret' :request.user.id , 'users':users }
    return render(request, 'bu/chat.html' , context)

###########################Profile#################### 

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
    user = get_object_or_404(FacultyStaff, pk=user_id)
    if user.cv:
        cv = user.cv  
        response = FileResponse(cv, content_type='application/pdf') 
        response['Content-Disposition'] = f'inline; filename="{user.first_name}-CV.pdf"'  # Provide a filename
        return response
    # If the user doesn't have a CV or the CV is not found, return a 404 error
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
                return redirect('business_unit_account:profile')
            
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
                        return redirect('business_unit_account:edit-profile')
                   
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

    return redirect('business_unit_account:edit-profile')

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

###########################Faculty#####################
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
def facultyinfo_view(request,faculty_id):
    faculty_member = get_object_or_404(FacultyStaff, id=faculty_id)
    collage_id = faculty_member.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    return render(request, 'bu/faculty-view.html', {'faculty_member': faculty_member , 'collagename': collagename})

###########################Traning Program#############

@login_required
def traningprogram_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    programs = Trainingprogram.objects.filter(collageid=collage_id)
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
    bu_programs = Trainingprogram.objects.filter(collageid=collage_id, isbuaccepted=True).order_by('-dataoffacultyproposal')
    faculty_or_staff_programs = Trainingprogram.objects.filter(collageid=collage_id, initiatedby='FacultyOrStaff', isbuaccepted=False)
    

    for program in faculty_or_staff_programs:
        try:
            faculty_staff = FacultyStaff.objects.get(id = program.programleader)
            name = faculty_staff.first_name +' '+faculty_staff.last_name
            program.Requestername = name
        except FacultyStaff.DoesNotExist:
            program.Requestername = ''
 
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
        pricefortrainee = request.POST.get('pricefortrainee')
        isOnline = request.POST.get('isonline')
        openToAllCheckbox = request.POST.get('openToAllCheckbox')

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

        if num_ofinstructors == '1' or num_ofinstructors == 1: 
                tempStatus="تم ارسال الطلب إلى المدرب"
                tempStatus2="انتظار قبول الطلب من قبل المدرب"
                tempStatus3= "تم قبول الطلب من قبل المدرب"
        else:
                tempStatus="تم ارسال الطلب إلى المدربين"
                tempStatus2="انتظار قبول الطلب من قبل جميع المدربين"
                tempStatus3="تم قبول الطلب من قبل جميع المدربين"


        if openToAllCheckbox:
            print("instructor sent to all faculty")
            new_program = Trainingprogram( 
                isonline = isOnline,           
                programtype=programtype,
                appourtunityopentoall=True,
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
                attachment_name=attachment_name,
                collageid=collage_id,
                isfacultyfound= False,
                iskaiaccepted=False,
                isreleased_field=False,
                isbuaccepted=True,
                totalcost = pricefortrainee,
                initiatedby='bu',
                status='فتح الفرصة للجميع',
                dataoffacultyproposal = timezone.now().date())
            new_program.save()

            new_StatusDateCheck =StatusDateCheck(
                status="إنشاء الطلب من قبل وحدة الأعمال",
                date=timezone.now().date(),
                indicator='T',
                training_program=new_program)
            new_StatusDateCheck.save()

            new_StatusDateCheck2 =StatusDateCheck(
                status="فتح التقديم لتقديم البرنامج لأعضاء هيئة التدريس ",
                date=timezone.now().date(),
                indicator='T',
                training_program=new_program)
            new_StatusDateCheck2.save()

            new_StatusDateCheck3 =StatusDateCheck(
                status="تم فرز الطلبات واختيار فريق البرنامج",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck3.save()

            new_StatusDateCheck4 =StatusDateCheck(
                status="تم ارسال الطلب إلى المعهد",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck4.save()

            new_StatusDateCheck5 =StatusDateCheck(
                status="انتظار قبول المعهد",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck5.save()

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

            new_StatusDateCheck8 =StatusDateCheck(
                status="انتهى تسجيل المتدربين",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck8.save()

            new_StatusDateCheck9 =StatusDateCheck(
                status="بدأ البرنامج",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck9.save()

            new_StatusDateCheck10 =StatusDateCheck(
                status="إنتهاء البرنامج",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck10.save()

            new_StatusDateCheck11 =StatusDateCheck(
                status="إصدار الشهادات",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck11.save()

            return redirect('business_unit_account:traning-program')
        else:
            new_program = Trainingprogram(
                isonline = isOnline,
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
                attachment_name=attachment_name,
                collageid=collage_id,
                isfacultyfound= False,
                iskaiaccepted=False,
                isreleased_field=False,
                isbuaccepted=True,
                initiatedby='bu',
                status=tempStatus2,
                totalcost = pricefortrainee,
                dataoffacultyproposal = timezone.now().date()
            )
            new_program.save()

            for instructor_id in instructors_id:
                try:
                    instructor = FacultyStaff.objects.get(id=instructor_id)
                    new_IdStatusDate = IdStatusDate(
                        instructor=instructor,
                        status="في انتظار قبول المدرب",
                        date=timezone.now().date(),
                        training_program=new_program)
                    new_IdStatusDate.save()
                except ObjectDoesNotExist:
                    print(f'Faculty_Staff with id {instructor_id} does not exist')


                id_status_dates_for_new_program = IdStatusDate.objects.filter(training_program=new_program)
                for instance in id_status_dates_for_new_program:
                    print(f'instructor id: {instance.instructor.id}, status: {instance.status}, date: {instance.date}')

        
            new_StatusDateCheck =StatusDateCheck(
                status="إنشاء الطلب من قبل وحدة الأعمال",
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
                status="إصدار الشهادات",
                date=None,
                indicator='W',
                training_program=new_program)
            new_StatusDateCheck10.save()

            print("case 2")
            return redirect('business_unit_account:traning-program')

    return render(request, 'bu/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain , 'bu_programs':bu_programs ,'faculty_or_staff_programs':faculty_or_staff_programs  })

@login_required
def delete_course(request, value_to_delete):
    program = Trainingprogram.objects.get(programid=value_to_delete)

    if program:
        program.delete()
    else:
        messages.error(request, 'No values to delete.')

    return redirect('business_unit_account:traning-program')

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
    waitingforaccept = IdStatusDate.objects.filter(status='في انتظار قبول المدرب' , training_program=editprogram ).count()
    IdStatusDateAccept = IdStatusDate.objects.filter( training_program=editprogram, status= "تم قبول الطلب من قبل المدرب").count()
    numofreq_instructors = IdStatusDateAccept + waitingforaccept
   
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
        pricefortrainee = request.POST.get('pricefortrainee')
        isOnline = request.POST.get('isonline')
    
        if isOnline == "online" :
            isOnline = True
        else:
            isOnline = False

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
        

        IdStatusDateAccept = IdStatusDate.objects.filter(training_program=editprogram, status= "تم قبول الطلب من قبل المدرب").count()
        editprogram_num_instructors = int(editprogram.num_ofinstructors)
      
        if IdStatusDateAccept == editprogram_num_instructors:
            status_check= StatusDateCheck.objects.filter(training_program=editprogram)
            status_check.filter(status="انتظار قبول الطلب من قبل جميع المدربين").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T')
            # status_check.filter(status='تم ارسال الطلب إلى المعهد').update(indicator='T')
            checkKAI = status_check.filter(status='تم ارسال الطلب إلى المعهد').get()
            if checkKAI.indicator == 'W':
                status_check.filter(status='تم ارسال الطلب إلى المعهد').update(indicator='C')
            
            IdStatusDeletetheRest = IdStatusDate.objects.filter(training_program = editprogram, status= 'في انتظار قبول المدرب')
            for id  in IdStatusDeletetheRest:
                id.delete()
                editprogram.instructorid.remove(id.instructor_id)

            IdStatusDeletetheRest2 = IdStatusDate.objects.filter(training_program = editprogram, status= "تم رفض الطلب من قبل المدرب")
            for id  in IdStatusDeletetheRest2:
                id.delete()
                editprogram.instructorid.remove(id.instructor_id)
        else:
            status_check= StatusDateCheck.objects.filter(training_program=editprogram)
            status_check.filter(status="انتظار قبول الطلب من قبل جميع المدربين").update(indicator='C')
            status_check.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='W')
            status_check.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='W')
            status_check.filter(status='تم ارسال الطلب إلى المعهد').update(indicator='W')
          
        editprogram.save()
        return redirect('business_unit_account:program_view' , program_id = editprogram.programid )

    return render(request, 'bu/TraningProgram-edit.html', {'IdStatusDateAccept':IdStatusDateAccept, 'numofreq_instructors':numofreq_instructors, 'waitingforaccept':waitingforaccept , 'program':editprogram ,'faculty':faculty , 'domain':domain ,  'id_status_dates' : id_status_dates, 'programflow':programflow })

def view_programfile(request, program_id):
    document = get_object_or_404(Trainingprogram, pk=program_id)
    
    if document.attachment:
        attachment_name = document.attachment_name
        file_extension = attachment_name.split('.')[-1] if '.' in attachment_name else ''
        content_type, _ = mimetypes.guess_type(attachment_name)
        
        if content_type:
            response = HttpResponse(document.attachment, content_type=content_type)
        else:
            # Define content type based on the file extension
            if file_extension.lower() == 'pdf':
                response = HttpResponse(document.attachment, content_type='application/pdf')
            elif file_extension.lower() == 'pptx':
                response = HttpResponse(document.attachment, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            elif file_extension.lower() in ['doc', 'docx']:
                response = HttpResponse(document.attachment, content_type='application/msword')
            else:
                # Set a default content type if the file extension is not recognized
                response = HttpResponse(document.attachment, content_type='application/octet-stream')
                
        response['Content-Disposition'] = f'inline; filename="{attachment_name}"'
        return response
    
    # If the document doesn't exist or the file data is missing, return a 404 error
    raise Http404("Document not found")

@login_required
def program_view(request , program_id):
    user = request.user
    program = get_object_or_404(Trainingprogram, programid=program_id)
    instructors = program.instructorid

    if program.programleader:
        Requestername = FacultyStaff.objects.get(id = program.programleader)
        name = Requestername.first_name +' '+Requestername.last_name
        program.Requestername = name
   
    
    instructors_id = program.instructorid
    if instructors_id :
        instructor_names = []
        for instructors in instructors_id:
            try:
                faculty_staff = FacultyStaff.objects.get(id=instructors)
                name = [faculty_staff.first_name +' '+faculty_staff.last_name , faculty_staff.id , faculty_staff.major , faculty_staff.email ]
                instructor_names.append(name)
            except FacultyStaff.DoesNotExist:
                instructor_names.append("")
        program.instructor_names = instructor_names

    Registertraniees = Register.objects.filter(programid=program_id)
    traniees_names = []
    for register in Registertraniees:
        try:
            traniee_info = Trainees.objects.get(id=register.id.id)
            name = [traniee_info.fullnamearabic , 
                     traniee_info.email, 
                     traniee_info.phonenumber,
                     traniee_info.nationalid, 
                     traniee_info.gender, 
                     register.haspaid , 
                     register.hasattended , 
                     register.refundrequsted ,
                     register.registerid ]
            traniees_names.append(name)
        except Trainees.DoesNotExist:
            traniees_names.append("")

    program.traniees_names = traniees_names

    Registertraniees = Register.objects.filter(programid=program_id ,haspaid = True )
    traniees_paid = []
    for register in Registertraniees:
        try:
            traniee_info = Trainees.objects.get(id=register.id.id)
            name = [traniee_info.fullnamearabic ,
                     register.haspaid ,
                       register.id.id ,
                         register.certifications ,
                         register.registerid]
            traniees_paid.append(name)
        except Trainees.DoesNotExist:
            traniees_paid.append("")

    program.traniees_paid = traniees_paid
  
    # get info for workflow
    id_status_dates = IdStatusDate.objects.filter(training_program=program)
    programflow = StatusDateCheck.objects.filter(training_program=program)
   
    if 'تم فرز الطلبات واختيار فريق البرنامج' in programflow:
        forall = True
    else:
        forall = False

    applicationidcount = IdStatusDate.objects.filter(status='participationRequest').count()
    waitingforaccept = IdStatusDate.objects.filter(status='في انتظار قبول المدرب' , training_program=program_id ).count()
    IdStatusDateRejectionValues = IdStatusDate.objects.filter(training_program=program_id, status= "تم رفض الطلب من قبل المدرب")
    IdStatusDateRejection = IdStatusDate.objects.filter( training_program=program_id, status= "تم رفض الطلب من قبل المدرب").count()
    IdStatusDateAccept = IdStatusDate.objects.filter( training_program=program_id, status= "تم قبول الطلب من قبل المدرب").count()
    faculty_members = FacultyStaff.objects.filter(collageid=program.collageid)
    numofreq = IdStatusDateAccept + waitingforaccept
    newinstructors = program.num_ofinstructors - numofreq 
   
    return render(request, 'bu/TraningProgram-view.html', {'newinstructors':newinstructors, 'numofreq':numofreq  ,'forall':forall,'user':user,'waitingforaccept':waitingforaccept,'IdStatusDateAccept':IdStatusDateAccept, 'program': program ,'id_status_dates': id_status_dates , 'programflow' : programflow , 'applicationidcount':applicationidcount,'IdStatusDateRejectionValues':IdStatusDateRejectionValues, 'IdStatusDateRejection': IdStatusDateRejection , 'faculty_members':faculty_members})

@login_required
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
    
@login_required
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
            program.status = "تحت الدراسة من قبل وحدة الأعمال"
        elif status_value == "accept":
            program.status = "تم قبول الطلب من قبل وحدة الأعمال"
        elif status_value == "reject":
            program.status = "تم الرفض من قبل وحدة الأعمال"
        
        program.save()

        for program in programs:
            instructor_id = program.instructorid
            try:
                faculty_staff = FacultyStaff.objects.get(id=instructor_id)
                program.instructor_first_name = faculty_staff.first_name
                program.instructor_last_name = faculty_staff.last_name
            except FacultyStaff.DoesNotExist:
                program.instructor_first_name = ""
                program.instructor_last_name = ""
        # return redirect('business_unit_account:program_view' , program_id = program.programid)
        return redirect('business_unit_account:traning-program')
        # return render(request, 'bu/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain })

@login_required
def haspaid(request, register_id):
        print('here1')
        try:
            trainee = Register.objects.get(registerid=register_id) 
            if trainee.haspaid:
                trainee.haspaid = False
            else:
                trainee.haspaid = True
            
            trainee.save()
            return JsonResponse({'success_message': trainee.haspaid })

        except Register.DoesNotExist:
            print('here2')
            return JsonResponse({'error_message': 'Register not found'})

        except Exception as e:
            print('here3')
            return JsonResponse({'error_message': f'An error occurred: {e}'})

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
def sendtokai(request, programid):
    if request.method == 'POST':
            program = Trainingprogram.objects.get(programid=programid)
            program.isbuaccepted = True
            program.status= "تم ارسال الطلب إلى المعهد"
            program.isfacultyfound=True
            program.save()
            status_check= StatusDateCheck.objects.filter(training_program=program)
            status_check.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل المعهد").update(indicator='C')
            status_check.filter(status="تم ارسال الطلب إلى المعهد").update(date=timezone.now().date() , indicator='T')
            return redirect('business_unit_account:program_view' , program_id = program.programid)

@login_required
def publish1(request, program_id):
    program = Trainingprogram.objects.get(programid=program_id)

    if request.method == 'POST':
        last_enrollment_date = request.POST.get('lastenrollmentdate')
        description = request.POST.get('description')
        attachment = request.POST.get('attachment')
        topic_english = request.POST.get('topic_english')
        description_english = request.POST.get('description_english')
        location = request.POST.get('location')
 
        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = program.attachment
            attachment_name = program.attachment_name
                
        if last_enrollment_date:
            last_enrollment_date = datetime.strptime(last_enrollment_date, "%Y-%m-%d").date()

        # Update the program
        program.location_field = location
        program.topic_english = topic_english
        program.programdescription_english = description_english
        program.lastenrollmentdate = last_enrollment_date
        program.programdescription = description
        program.attachment = attachment
        program.attachment_name = attachment_name
        program.status="تم نشر البرنامج "
        program.isreleased_field = True
        print('here')
        program.save()

        status_check= StatusDateCheck.objects.filter(training_program=program)

        status_check.filter(status="تم نشر البرنامج ").update(indicator='T')
        status_check.filter(status="تم نشر البرنامج ").update(date=timezone.now().date())
        return redirect('business_unit_account:program_view' , program_id = program.programid)

@login_required
@require_POST
def select_program_team(request, program_id):
    program = get_object_or_404(Trainingprogram, programid=program_id)
    selected_instructors = request.POST.getlist('trainer_selection')
    
    # Update the instructors for the program
    old_set = set(program.instructorid) if program.instructorid else set()
    new_set = set([int(id) for id in selected_instructors])
    program.instructorid = list(old_set.union(new_set))

    program.appourtunityopentoall = False
    program.status="تم فرز الطلبات واختيار فريق البرنامج" 
    program.save()

    update_status = IdStatusDate.objects.filter(training_program=program)
    for id in  selected_instructors:
        update_status.filter(instructor_id=id).update(status="تم قبول الطلب من قبل المدرب")


    status_check= StatusDateCheck.objects.filter(training_program=program_id)
    status_check.filter(status="تم فرز الطلبات واختيار فريق البرنامج").update(indicator='T' , date=timezone.now().date())
    status_check.filter(status="تم ارسال الطلب إلى المعهد").update(indicator='C')
 
    return redirect('business_unit_account:program_view' , program_id = program.programid)

# this view in case instructor have rejected
@login_required
def send_to_new_trainee(request, program_id , instructor_id):
    if request.method == 'POST':
        try:
            # Get the program from the database
            training_program = Trainingprogram.objects.get(programid=program_id)
            instructorTodelete = IdStatusDate.objects.get(instructor=instructor_id, training_program=training_program)
            instructorTodelete.delete()

            # Get the new instructors from the form
            new_instructors = request.POST.get('instructor')
          
            if new_instructors not in training_program.instructorid:
                    training_program.instructorid.append(new_instructors)
                    training_program.save()
            # Create new id_status_date for each new instructor
                    IdStatusDate.objects.create(
                        instructor_id=new_instructors,
                        status="في انتظار قبول المدرب",
                        date=None,
                        training_program=training_program)            
            program = training_program
            return redirect('business_unit_account:program_view' , program_id = program.programid)
        except Trainingprogram.DoesNotExist as e:
            print("Training program not found:", e)
            return HttpResponse("Training program not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
    return HttpResponse("Unexpected error or GET request")

# this view in case BU want to request instructor/s form a faculty requset
@login_required
def send_to_new_trainees2(request, program_id):
    if request.method == 'POST':
        try:
            # Get the program from the database
            training_program = Trainingprogram.objects.get(programid=program_id)
            training_program.status=  "انتظار قبول الطلب من قبل جميع المدربين"
            # Get the new instructors from the form
            new_instructors = request.POST.getlist('instructor')
            openToAllCheckbox = request.POST.get('openToAllCheckbox')

            if openToAllCheckbox:
                print("send to new trainee case 1")
                training_program.status='فتح الفرصة للجميع'
                training_program.appourtunityopentoall=True
                training_program.save()
                new_StatusDateCheck2= StatusDateCheck.objects.filter(training_program=program_id)
                new_StatusDateCheck2.filter(status="فتح التقديم لتقديم البرنامج لأعضاء هيئة التدريس ").update(indicator='T' , date=timezone.now().date())
                
                new_StatusDateCheck3 = StatusDateCheck(
                        status="تم فرز الطلبات واختيار فريق البرنامج",
                        date=None,
                        indicator='W',
                        training_program=training_program)
                new_StatusDateCheck3.save()
            else:
                print("send to new trainee case 2")
            # Add new instructor ids to the training program
                for instructor_id in new_instructors:
                        instructor_id = int(instructor_id)
                        if instructor_id not in training_program.instructorid:
                            training_program.instructorid.append(instructor_id)
                        training_program.save()

            # Create new id_status_date for each new instructor
                for instructor_id in new_instructors:
                    IdStatusDate.objects.create(
                        instructor_id=instructor_id,
                        status="في انتظار قبول المدرب",
                        date=None,
                        training_program=training_program
                    )
            program=training_program
            return redirect('business_unit_account:program_view' , program_id = program.programid)
        except Trainingprogram.DoesNotExist:
            print("Training program not found:", e)
         
        except Exception as e:
            print("An error occurred:", e)
           
    print("Didn't enter POST request handling")

# this case if BU want to have more instructor  
@login_required
def send_to_new_trainee3(request, program_id):
    if request.method == 'POST':
        try:
            # Get the program from the database
            training_program = Trainingprogram.objects.get(programid=program_id)

            # Get the new instructors from the form
            new_instructors = request.POST.get('instructor')
          
            if new_instructors not in training_program.instructorid:
                    training_program.instructorid.append(new_instructors)
                    training_program.save()
            # Create new id_status_date for each new instructor
                    IdStatusDate.objects.create(
                        instructor_id=new_instructors,
                        status="في انتظار قبول المدرب",
                        date=None,
                        training_program=training_program)            
            program = training_program
            return redirect('business_unit_account:program_view' , program_id = program.programid)
        except Trainingprogram.DoesNotExist as e:
            print("Training program not found:", e)
            return HttpResponse("Training program not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
    return HttpResponse("Unexpected error or GET request")

@login_required
def accepte_facultyprogram(request, program_id):
    program = get_object_or_404(Trainingprogram, programid=program_id)
    program.status = "تم قبول الطلب من قبل وحدة الأعمال"
    program.isbuaccepted=True
    print(program.programid)

    tempStatus="تم ارسال الطلب إلى وحدة الاعمال"
    tempStatus2="انتظار قبول الطلب من قبل وحدة الاعمال"
    tempStatus3= "تم قبول الطلب من قبل وحدة الاعمال"

    program.save()
    status_check= StatusDateCheck.objects.filter(training_program=program_id)
    print(status_check)
    status_check.filter(status = tempStatus3 ).update(indicator = 'T',date = timezone.now().date())
    status_check.filter(status = tempStatus2 ).update(indicator = 'T')

    if program.num_ofinstructors == 1 or program.num_ofinstructors == '1':
        status_check.filter(status = "تم ارسال الطلب إلى المعهد" ).update(indicator = 'C')
    return redirect('business_unit_account:program_view' , program_id = program.programid)
    
@login_required
@require_POST
def rejecte_facultyprogram(request, program_id):
    rejection_reason = request.POST.get('rejectionReason')
    program = get_object_or_404(Trainingprogram, programid=program_id)
    program.status ="تم رفض الطلب من قبل وحدة الأعمال"
    program.rejectionresons=rejection_reason
    program.isbuaccepted=False
    program.dataofburejection=datetime.now().date()
    program.save()
    return redirect('business_unit_account:traning-program')

@login_required
def deleteWaittingInstructor(request,id):
    try:
        instructorTodelete = IdStatusDate.objects.get(id =id)
        program = instructorTodelete.training_program
        instructor_id = instructorTodelete.instructor_id
        instructorTodelete.delete()

        # Remove instructor's id from the instructorid array in the associated TrainingProgram object
        program.instructorid = [id for id in program.instructorid if id != instructor_id]
        program.save()

        waitingforaccept = IdStatusDate.objects.filter(status='في انتظار قبول المدرب' , training_program=program ).count()
        IdStatusDateAccept = IdStatusDate.objects.filter( training_program=program, status= "تم قبول الطلب من قبل المدرب").count()
        numofreq_instructors = IdStatusDateAccept + waitingforaccept

        return JsonResponse({'success1': str(waitingforaccept) , 'success2': str(numofreq_instructors)  })
    except IdStatusDate.DoesNotExist:
        print('here2')
        return JsonResponse({'error_message': 'IdStatusDate not found'})

    except Exception as e:
        print('here3')
        return JsonResponse({'error_message': f'An error occurred: {e}'})

#####################Project###################

def view_projectfile(request, program_id, file_id):
    file = get_object_or_404(Files, fileid=file_id, project=program_id)

    attachment_name = file.attachment_name
    file_extension = attachment_name.split('.')[-1] if '.' in attachment_name else ''
    content_type, _ = mimetypes.guess_type(attachment_name)

    if content_type:
        content_type_header = content_type
    else:
        if file_extension.lower() == 'pdf':
            content_type_header = 'application/pdf'
        elif file_extension.lower() == 'pptx':
            content_type_header = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif file_extension.lower() in ['doc', 'docx']:
            content_type_header = 'application/msword'
        else:
            content_type_header = 'application/octet-stream'

    response = HttpResponse(file.attachment, content_type=content_type_header)
    response['Content-Disposition'] = f'inline; filename="{attachment_name}"'
    return response

@login_required
def projects_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    projects = Project.objects.filter(collageid=collage_id)
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    bu_programs = Project.objects.filter(collageid=collage_id).order_by('-OfferingDate')

  
    if request.method == 'POST':
        Name = request.POST.get('topic')
        # TotalCost = request.POST.get('price')
        programtype = request.POST.get('domain')
        team_id = request.POST.getlist('instructor')
        end_date = request.POST.get('enddate')
        companyName = request.POST.get('CompanyName')
        QuestionDeadline = request.POST.get('questionDate')
        EtimadDeadline = request.POST.get('companyDate')
        ProposalSubmissionDeadline = request.POST.get('proposalSubmission')
        contractDuration = request.POST.get('duration')
        durationType = request.POST.get('durationType') 
        # EnvelopeOpening = request.POST.get('envelopeDate')
        num_ofteam = request.POST.get('num_ofinstructors')
        openToAllCheckbox = request.POST.get('openToAllCheckbox')
        project_description = request.POST.get('subject')


        attachment_data = []
        if 'attachment' in request.FILES:
            attachments = request.FILES.getlist('attachment')

            for attachment_file in attachments:
                attachment_data.append({
                    'content': attachment_file.read(),
                    'name': attachment_file.name,
                })
    

        tempStatus="تم ارسال الطلب إلى الفريق"
        tempStatus2="انتظار قبول الطلب من قبل جميع الفريق"
        tempStatus3="تم قبول الطلب من قبل جميع الفريق"


        if openToAllCheckbox:
            print("instructor sent to all faculty")
            new_project = Project( 
                Name = Name,
                # totalcost = TotalCost,
                collageid=collage_id,
                Teamid = team_id,
                enddate=end_date,
                status ='فتح الفرصة للجميع',
                CompanyName = companyName,
                OfferingDate = date.today(),
                QuestionDeadline = None if not QuestionDeadline else QuestionDeadline,
                EtimadDeadline = None if not EtimadDeadline else EtimadDeadline,
                ProposalSubmissionDeadline = None if not ProposalSubmissionDeadline else ProposalSubmissionDeadline,
                contractDuration = contractDuration,
                durationType = durationType,
                # EnvelopeOpening = EnvelopeOpening,
                num_ofTeam = num_ofteam,         
                programtype=programtype,
                appourtunityopentoall=True,
                description = project_description)
            new_project.save()

            if attachment_data:
                for attachmentt in attachment_data:
                    new_file = Files(
                            attachment = attachmentt['content'],
                            attachment_name = attachmentt['name'],
                            project = new_project
                    )
                    new_file.save()

            new_StatusDateCheck =StatusDateCheckProject(
                status="إنشاء المشروع",
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck.save()

            new_StatusDateCheck2 =StatusDateCheckProject(
                status="فتح الانضمام للمشروع لأعضاء هيئة التدريس ",
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck2.save()

            new_StatusDateCheck3 =StatusDateCheckProject(
                status="تم فرز الطلبات واختيار فريق العمل",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck3.save()

            new_StatusDateCheck4 =StatusDateCheckProject(
                status="اختيار رئيس الفريق",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck4.save()

            new_StatusDateCheck5 =StatusDateCheckProject(
                status=" تم بدء العمل على المشروع ",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck5.save()

            # new_StatusDateCheck6 =StatusDateCheckProject(
            #     status="آخر تاريخ لتسليم المشروع للمراجعة من قبل المعهد",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck6.save()

            # new_StatusDateCheck7 =StatusDateCheckProject(
            #     status="تسليم المشروع للمعهد للمراجعة",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck7.save()

            new_StatusDateCheck8 =StatusDateCheckProject(
                status="المراجعة من قبل المعهد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck8.save()

            # new_StatusDateCheck9 =StatusDateCheckProject(
            #     status="التاريخ المتوقع للرد على المشروع",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck9.save()

            new_StatusDateCheck10 =StatusDateCheckProject(
                status="حالة المشروع بعد الرد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck10.save()

            return redirect('business_unit_account:projects')
        else:
            new_project = Project( 
                Name = Name,
                collageid=collage_id,
                Teamid = team_id,
                enddate=end_date,
                status =tempStatus2,
                CompanyName = companyName,
                OfferingDate = date.today(),
                QuestionDeadline = QuestionDeadline,
                EtimadDeadline = EtimadDeadline,
                ProposalSubmissionDeadline = ProposalSubmissionDeadline,
                contractDuration = contractDuration,
                durationType = durationType,
                num_ofTeam = num_ofteam,         
                programtype=programtype,
                appourtunityopentoall=True,
                description = project_description)
            new_project.save()

            for attachmentt in attachment_data:
                new_file = Files(
                           attachment = attachmentt['content'],
                           attachment_name = attachmentt['name'],
                           project = new_project
                )
                new_file.save()

            for team in team_id:
                try:
                    member = FacultyStaff.objects.get(id=team)
                    new_IdStatusDate = IdStatusDate(
                        instructor=member,
                        status="في انتظار قبول العضو",
                        date=timezone.now().date(),
                        project=new_project)
                    new_IdStatusDate.save()
                except ObjectDoesNotExist:
                    print(f'Faculty_Staff with id {member} does not exist')


                id_status_dates_for_new_program = IdStatusDate.objects.filter(project=new_project)
                for instance in id_status_dates_for_new_program:
                    print(f'instructor id: {instance.instructor.id}, status: {instance.status}, date: {instance.date}')

            new_StatusDateCheck =StatusDateCheckProject(
                status="إنشاء المشروع",
                date=timezone.now().date(),
                indicator='T',# means finished
                project=new_project)
            new_StatusDateCheck.save()

            new_StatusDateCheck2 =StatusDateCheckProject(
                status=tempStatus,
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck2.save()

            new_StatusDateCheck3 =StatusDateCheckProject(
                status=tempStatus2,
                date=None,
                indicator='C',#waiting C: current,  F: fail 
                project=new_project)
            new_StatusDateCheck3.save()

            new_StatusDateCheck4 =StatusDateCheckProject(
                status=tempStatus3,
                date=None,
                indicator='W',#waiting C: current,  F: fail 
                project=new_project)
            new_StatusDateCheck4.save()

            new_StatusDateCheck5 =StatusDateCheckProject(
                status="اختيار رئيس الفريق",
                date=None,
                indicator='W',#waiting C: current,  F: fail 
                project=new_project)
            new_StatusDateCheck5.save()

            new_StatusDateCheck6 =StatusDateCheckProject(
                status=" تم بدء العمل على المشروع ",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck6.save()

            # new_StatusDateCheck7 =StatusDateCheckProject(
            #     status="آخر تاريخ لتسليم المشروع للمراجعة من قبل المعهد",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck7.save()

            # new_StatusDateCheck8 =StatusDateCheckProject(
            #     status="تسليم المشروع للمعهد للمراجعة",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck8.save()

            new_StatusDateCheck9 =StatusDateCheckProject(
                status="المراجعة من قبل المعهد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck9.save()

            # new_StatusDateCheck10 =StatusDateCheckProject(
            #     status="التاريخ المتوقع للرد على المشروع",
            #     date=None,
            #     indicator='W',
            #     project=new_project)
            # new_StatusDateCheck10.save()

            new_StatusDateCheck11 =StatusDateCheckProject(
                status="حالة المشروع بعد الرد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck11.save()

            print("case 2")
            return redirect('business_unit_account:projects')

    return render(request, 'bu/Projects.html', {'user': user , 'programs':projects,'faculty':faculty, 'bu_programs':bu_programs})

@login_required
def delete_project(request, value_to_delete):
    project = Project.objects.get(programid=value_to_delete)

    if project:
        project.delete()
    else:
        messages.error(request, 'No values to delete.')

    return redirect('business_unit_account:projects')

@login_required
def edit_project(request, value_to_edit):
    editproject = Project.objects.get(programid=value_to_edit)
    user = request.user
    collage_id = user.collageid.collageid
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)

    id_status_dates = IdStatusDate.objects.filter(project=editproject)
    programflow = StatusDateCheckProject.objects.filter(project=editproject)
    waitingforaccept = IdStatusDate.objects.filter(status="في انتظار قبول العضو", project=editproject ).count()
    IdStatusDateAccept = IdStatusDate.objects.filter( project=editproject, status= "تم قبول الطلب من قبل العضو").count()
    numofreq_instructors = IdStatusDateAccept + waitingforaccept
   
    edit_file = Files.objects.filter(project=editproject)
    attachment_data = []
    
    if request.method == 'POST':
        Name = request.POST.get('topic')
        programtype = request.POST.get('domain')
        end_date = request.POST.get('enddate')
        CompanyName = request.POST.get('CompanyName')
        QuestionDeadline = request.POST.get('questionDate')
        EtimadDeadline = request.POST.get('companyDate')
        ProposalSubmissionDeadline = request.POST.get('proposalSubmission')
        contractDuration = request.POST.get('duration')
        durationType = request.POST.get('durationType') 
        num_ofteam = request.POST.get('num_ofteam')
        project_description = request.POST.get('subject')

       
        if 'attachment' in request.FILES:
            attachments = request.FILES.getlist('attachment')
            for attachment in attachments:
                try:
                    # Validate file extension
                     FileExtensionValidator(allowed_extensions=['pdf', 'pptx', 'doc', 'docx', 'xlsx'])(attachment)
                     attachment_data.append({
                         'name': attachment.name,
                         'content': attachment.read(),
                     })
                except ValidationError as e:
                     # Handle invalid file extension
                     error_message = f'Invalid file extension for {attachment.name}. Allowed extensions: pdf, pptx, doc, docx, xlsx.'
                     return HttpResponseBadRequest(error_message)
        else:
             for edit_file_instance in edit_file:
                 attachment_data.append({
             'name': edit_file_instance.attachment_name,
             'content': edit_file_instance.attachment.read(),
         })
     
        editproject.Name=Name
        editproject.programtype = programtype
        editproject.enddate=end_date
        editproject.CompanyName=CompanyName
        # editproject.QuestionDeadline=QuestionDeadline
        # editproject.EtimadDeadline=EtimadDeadline
        # editproject.ProposalSubmissionDeadline=ProposalSubmissionDeadline
        editproject.QuestionDeadline = None if not QuestionDeadline else QuestionDeadline
        editproject.EtimadDeadline = None if not EtimadDeadline else EtimadDeadline
        editproject.ProposalSubmissionDeadline = None if not ProposalSubmissionDeadline else ProposalSubmissionDeadline
        editproject.contractDuration=contractDuration
        editproject.durationType=durationType
        editproject.num_ofTeam=num_ofteam
        editproject.description = project_description

        if  attachment_data:         
            for attachment_data in attachment_data:
                    try:
            # Assuming edit_file is a QuerySet, get the individual object
                        edit_file_instance = edit_file.get(attachment_name=attachment_data['name'])
            # Update attributes of the individual object
                        edit_file_instance.attachment = attachment_data['content']
                        edit_file_instance.project = editproject
                        edit_file_instance.save()
                    except edit_file.model.DoesNotExist:
            # If the file doesn't exist, create a new one
                        edit_file_instance = Files(
                        attachment=attachment_data['content'],
                        attachment_name=attachment_data['name'],
                        project=editproject)
                        edit_file_instance.save()

    # Save the changes to the individual object
        IdStatusDateAccept = IdStatusDate.objects.filter( project=editproject, status= "تم قبول الطلب من قبل العضو").count()
        editprogram_num_team= int(editproject.num_ofTeam)
      
        if IdStatusDateAccept == editprogram_num_team  and  editproject.status != 'تم قبول الطلب من قبل جميع الفريق':
            status_check= StatusDateCheckProject.objects.filter(project=editproject)
            status_check.filter(status="انتظار قبول الطلب من قبل جميع الفريق").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل العضو").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل جميع الفريق").update(indicator='T')
            status_check.filter(status="اختيار رئيس الفريق").update(indicator='C')
            editproject.status = 'تم قبول الطلب من قبل جميع الفريق'

            IdStatusDeletetheRest = IdStatusDate.objects.filter(project = editproject, status= 'في انتظار قبول العضو')
            for id  in IdStatusDeletetheRest:
                id.delete()
                editproject.Teamid.remove(id.instructor_id)

            IdStatusDeletetheRest2 = IdStatusDate.objects.filter(project = editproject, status= "تم رفض الطلب من قبل العضو")
            for id  in IdStatusDeletetheRest2:
                id.delete()
                editproject.Teamid.remove(id.instructor_id)
        else:
            status_check= StatusDateCheckProject.objects.filter(project=editproject)
            status_check.filter(status="انتظار قبول الطلب من قبل جميع الفريق").update(indicator='C')
            status_check.filter(status="تم قبول الطلب من قبل العضو").update(indicator='W')
            status_check.filter(status="تم قبول الطلب من قبل جميع الفريق").update(indicator='W')
            status_check.filter(status="اختيار رئيس الفريق").update(indicator='W')
          
        editproject.save()
        return redirect('business_unit_account:project_view' , program_id = editproject.programid )

    return render(request, 'bu/Projects-edit.html', {'IdStatusDateAccept':IdStatusDateAccept, 'numofreq_instructors':numofreq_instructors, 'waitingforaccept':waitingforaccept , 'program':editproject ,'faculty':faculty ,  'id_status_dates' : id_status_dates, 'programflow':programflow, 'files': edit_file })

@login_required
def project_view(request , program_id):
    user = request.user
    project = get_object_or_404(Project, programid=program_id)
    instructors = project.Teamid
    file = Files.objects.filter(project=program_id)

   
    instructors_id = project.Teamid
    if instructors_id :
        instructor_names = []
        for instructors in instructors_id:
            try:
                faculty_staff = FacultyStaff.objects.get(id=instructors)
                name = [faculty_staff.first_name +' '+faculty_staff.last_name , faculty_staff.id , faculty_staff.major , faculty_staff.email ]
                instructor_names.append(name)
            except FacultyStaff.DoesNotExist:
                instructor_names.append("")
        project.instructor_names = instructor_names
  
    # get info for workflow
    id_status_dates = IdStatusDate.objects.filter(project=project)
    programflow = StatusDateCheckProject.objects.filter(project=project)
   
    if 'تم فرز الطلبات واختيار فريق العمل' in programflow:
        forall = True
    else:
        forall = False

    applicationidcount = IdStatusDate.objects.filter(status='participationRequest', project=program_id ).count()
    print('applicationidcount' , applicationidcount)
    waitingforaccept = IdStatusDate.objects.filter(status='في انتظار قبول العضو' , project=program_id ).count()
    IdStatusDateRejectionValues = IdStatusDate.objects.filter(project=program_id, status= "تم رفض الطلب من قبل العضو")
    IdStatusDateRejection = IdStatusDate.objects.filter( project=program_id, status= "تم رفض الطلب من قبل العضو").count()
    IdStatusDateAccept = IdStatusDate.objects.filter( project=program_id, status= "تم قبول الطلب من قبل العضو").count()
    faculty_members = FacultyStaff.objects.filter(collageid=project.collageid)
    numofreq = IdStatusDateAccept + waitingforaccept
    newinstructors = project.num_ofTeam - numofreq 
   
    return render(request, 'bu/Projects-view.html', { 'applicationidcount':applicationidcount , 'newinstructors':newinstructors, 'numofreq':numofreq  ,'forall':forall,'user':user,'waitingforaccept':waitingforaccept,'IdStatusDateAccept':IdStatusDateAccept, 'program': project ,'id_status_dates': id_status_dates , 'programflow' : programflow,'IdStatusDateRejectionValues':IdStatusDateRejectionValues, 'IdStatusDateRejection': IdStatusDateRejection , 'faculty_members':faculty_members, 'files':file})

@login_required
@require_POST
def select_project_team(request, program_id):
    program = get_object_or_404(Project, programid=program_id)
    selected_instructors = request.POST.getlist('trainer_selection')
    leader_selection = request.POST.get('leader_selection')
    
    # Update the instructors for the program
    old_set = set(program.Teamid) if program.Teamid else set()
    new_set = set([int(id) for id in selected_instructors])
    program.Teamid = list(old_set.union(new_set))

    program.programleader = leader_selection
    program.appourtunityopentoall = False
    program.status = "تم بدء العمل على المشروع"
    program.save() 

    update_status = IdStatusDate.objects.filter(project=program)
    for id in  selected_instructors:
        update_status.filter(instructor_id=id).update(status="تم قبول الطلب من قبل العضو")

    status_check= StatusDateCheckProject.objects.filter(project=program_id)
    status_check.filter(status="تم فرز الطلبات واختيار فريق العمل").update(indicator='T' , date=timezone.now().date())
    status_check.filter(status="اختيار رئيس الفريق").update(indicator='T', date=timezone.now().date())
    status_check.filter(status=" تم بدء العمل على المشروع ").update(indicator='T', date=timezone.now().date())
 
    return redirect('business_unit_account:project_view' , program_id = program.programid)

# send to new member after someone reject
@login_required
def send_to_new_member(request, program_id , instructor_id):
    if request.method == 'POST':
        try:
            ('here in send_to_new_member')
            # Get the program from the database
            project = Project.objects.get(programid=program_id)
            instructorTodelete = IdStatusDate.objects.get(instructor=instructor_id, project=project)
            instructorTodelete.delete()

            # Get the new instructors from the form
            new_instructors = request.POST.get('instructor')
          
            if new_instructors not in project.Teamid:
                    project.Teamid.append(new_instructors)
                    project.save()
            # Create new id_status_date for each new instructor
                    IdStatusDate.objects.create(
                        instructor_id=new_instructors,
                        status="في انتظار قبول العضو",
                        date=None,
                        project=project)            
            program = project
            return redirect('business_unit_account:project_view' , program_id = program.programid)
        except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
    return HttpResponse("Unexpected error or GET request")

@login_required
def send_to_new_member3(request, program_id):
    if request.method == 'POST':
        try:
            # Get the program from the database
            project = Project.objects.get(programid=program_id)

            # Get the new instructors from the form
            new_instructors = request.POST.get('instructor')
          
            if new_instructors not in project.Teamid:
                    project.Teamid.append(new_instructors)
                    project.save()
            # Create new id_status_date for each new instructor
                    IdStatusDate.objects.create(
                        instructor_id=new_instructors,
                        status="في انتظار قبول العضو",
                        date=None,
                        project=project)            
            program = project
            return redirect('business_unit_account:project_view' , program_id = program.programid)
        except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
    return HttpResponse("Unexpected error or GET request")

import logging

logger = logging.getLogger(__name__)

@login_required
def deleteWaittingMember(request,id):
    try:
        instructorTodelete = IdStatusDate.objects.get(id =id)
        program = instructorTodelete.project
        instructor_id = instructorTodelete.instructor_id
        instructorTodelete.delete()

        # Remove instructor's id from the instructorid array in the associated TrainingProgram object
        program.Teamid = [id for id in program.Teamid if id != instructor_id]
        program.save()

        waitingforaccept = IdStatusDate.objects.filter(status='في انتظار قبول العضو' , project=program ).count()
        IdStatusDateAccept = IdStatusDate.objects.filter( project=program, status= "تم قبول الطلب من قبل العضو").count()
        numofreq_instructors = IdStatusDateAccept + waitingforaccept

        logger.info(f'waitingforaccept: {waitingforaccept}, numofreq_instructors: {numofreq_instructors}')

        return JsonResponse({'success1': str(waitingforaccept) , 'success2': str(numofreq_instructors)  })
    except IdStatusDate.DoesNotExist:
        logger.error('IdStatusDate not found')
        print('here2')
        return JsonResponse({'error_message': 'IdStatusDate not found'})

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        print('here3')
        return JsonResponse({'error_message': f'An error occurred: {e}'})

@login_required
def chooseleader(request, program_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(programid=program_id)

            leader = request.POST.get('leader')
            project.programleader = leader 
            status_check= StatusDateCheckProject.objects.filter(project=project)
            status_check.filter(status="اختيار رئيس الفريق").update(indicator='T', date=timezone.now().date())
            status_check.filter(status=" تم بدء العمل على المشروع ").update(indicator='T', date=timezone.now().date())
            project.status = "تم بدء العمل على المشروع"
            project.save() 

            program = project
            return redirect('business_unit_account:project_view' , program_id = program.programid)
        except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    return HttpResponse("Unexpected error or GET request")

