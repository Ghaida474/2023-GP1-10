import base64
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Kaibuemployee ,FacultyStaff,Collage, Trainingprogram,Register,Trainees,IdStatusDate, StatusDateCheck, Files, Project, StatusDateCheckProject, Notification ,  Task , TaskToUser, Admin
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

    bu = FacultyStaff.objects.get(collageid=user.collageid , is_buhead=True)
    print('------------------')
    url = "https://api.chatengine.io/chats/"
    payload = {
        "title": project.Name,
        "is_direct_chat": False,
        "usernames":usernamess
    }
    headers = {
        'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
        'User-Name': bu.username,
        'User-Secret': str(bu.id),
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

########################### Profile #################### 

@login_required
def business_unit_home (request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    success2 = False

    if collage.new_user:
        return redirect('business_unit_account:change_new_user_password')
    
    staff = collage.nostaff 
    faculty = collage.nofaculty
    
    if staff is None:
        staff=0

    if faculty is None:
        faculty=0

    emp = staff + faculty
    count = len(collage.departments)
    context = {'user': user , 'collage':collage , "emp":emp , 'department':count , 'success2':success2 }
    return render(request, 'bu/Home.html', context)

@login_required
def change_new_user_password(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        collage.password = make_password(new_password)
        collage.new_user = False
        collage.save()
        return redirect('business_unit_account:business_unit_home')
    return render(request, 'bu/new-use-reset-password.html')

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
 
    if request.method == 'POST':
        print('in changepassword_view')
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "تم تغيير كلمة المرور بنجاح.")
                return redirect('business_unit_account:profile')
    return render(request, 'bu/change-password.html', {'user': user, 'form': form})

@login_required
def changeBUpassword_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
 
    if request.method == 'POST':
            current_password = request.POST.get("current_password")
            confirm_password = request.POST.get("confirm_Password")
            new_password = request.POST.get("new_password")

            if not check_password(current_password, collage.password):
                error_message = "كلمة المرور الحالية غير صحيحة."
                return render(request, 'bu/change-password.html', {'error_message': error_message , 'user': user})

            if new_password != confirm_password:
                error_message = "كلمة المرور الجديدة وتأكيد كلمة المرور غير متطابقين."
                return render(request, 'bu/change-password.html', {'error_message': error_message, 'user': user})

            collage.password = make_password(new_password)
            collage.save()
            messages.success(request, "تم تغيير كلمة المرور بنجاح.")
            return redirect('business_unit_account:business_unit_home')


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


############Traningprograms#############

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
def traningprogram_view(request):
    user = request.user
    date_time=timezone.now() 
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())

    
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

            Notification.objects.create(

                        faculty_target=user,
                        training_program=new_program,
                        notification_message=F"تم إنشاء برنامج{new_program.topic} وتم فترح الفرصه لجميع اعضاء هيئة التدريس للمشاركة به الرجاء اختيار فريق العمل عند وجدد عدد كاف من المتقدمين ",
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
            if user.sendnotificationbyemail:
                        send_custom_email(request, member.email, "فرصه للمشاركة في برنامج تدريبي متاحة للجميع " ,"فرصه للمشاركة في برنامج تدريبي متاحة للجميع ")

            

            new_notification = Notification(
                        
                        training_program=new_program,
                        notification_message="فرصه للمشاركة في برنامج تدريبي متاحة للجميع ",
                         
                        need_to_be_opened=True,
                        function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
                        target_indicator=1, # this to indicate that notification is targeted to faculties 
                        need_to_be_shown=True,
            )
            new_notification.save()
            for member in faculty:
                if member.sendnotificationbyemail:
                        send_custom_email(request, member.email, "فرصه للمشاركة في برنامج تدريبي متاحة للجميع " ,"فرصه للمشاركة في برنامج تدريبي متاحة للجميع ")


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
                    date_time=timezone.now() 


                    status_message = f"يتم إرسال طلب من قبل وحدة الأعمال للمشاركة في برنامج تدريبي بعنوان {new_program.topic}. الرجاء الدخول إلى البرنامج وتحديد مشاركتك فيه أو عدم مشاركتك فيه."

                    new_notification = Notification(
                        faculty_target=instructor,
                        training_program=new_program,
                        notification_message=status_message,
                         
                        need_to_be_opened=True,
                        function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
                        need_to_be_shown=True,

                    )
                    new_notification.save()
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'طلب المشاركة في برنامج التدريب', status_message)




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
        
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
       )    
    
    faculty_or_staff_program_ids = faculty_or_staff_programs.values_list('programid', flat=True)

    # Get the program IDs from combined_programs
    combined_program_ids = [program.programid for program in bu_programs]

    # Filter notifications for faculty_or_staff_programs
    notifications_in_faculty_or_staff_programs = notifications_in_programs.filter(
                training_program__programid__in=faculty_or_staff_program_ids
            )

    # Filter notifications for combined_programs
    notifications_in_combined_programs = notifications_in_programs.filter(
                 training_program__programid__in=combined_program_ids
            )

    faculty_or_staff_program_ids = notifications_in_faculty_or_staff_programs.values_list(
                'training_program__programid', flat=True).distinct()

# Retrieve the programid(s) for combined programs
    combined_program_ids = notifications_in_combined_programs.values_list(
                  'training_program__programid', flat=True).distinct()
    
    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())
    return render(request, 'bu/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain , 'bu_programs':bu_programs ,'faculty_or_staff_programs':faculty_or_staff_programs , 'notifications_in_programs':notifications_in_programs , 'notifications_in_faculty_or_staff_programs':notifications_in_faculty_or_staff_programs, 'notifications_in_combined_programs':notifications_in_combined_programs , 'faculty_or_staff_program_ids':faculty_or_staff_program_ids, 'combined_program_ids':combined_program_ids,
                                                       'notifications_in_tasks':notifications_in_tasks})

@login_required
def delete_course(request, value_to_delete):
    program = Trainingprogram.objects.get(programid=value_to_delete)

    if program:
        date_time=timezone.now()
        for instructor_id in program.instructorid:
                try:
                    instructor = FacultyStaff.objects.get(id=instructor_id)

                    status_message = f"تم حذف البرنامج التدريبي {program.topic} من قبل وحدة الأعمال. "

                    new_notification = Notification(
                        faculty_target=instructor,
                        training_program=program,
                        notification_message=status_message,
                        need_to_be_shown=True,          
                    )
                    new_notification.save()
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'حذف برنامج التدريب', status_message)
                    program.delete()
                except ObjectDoesNotExist:
                    print(f'Faculty_Staff with id {instructor_id} does not exist')
    else:
        messages.error(request, 'No values to delete.')
    return redirect('business_unit_account:traning-program')

@login_required
def edit_program(request, value_to_edit):
    
    editprogram = Trainingprogram.objects.get(programid=value_to_edit)
    user = request.user
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())

    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())


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
        

        IdStatusDateAccept = IdStatusDate.objects.filter( training_program=editprogram, status= "تم قبول الطلب من قبل المدرب").count()
        editprogram_num_instructors = int(editprogram.num_ofinstructors)
      
        if IdStatusDateAccept == editprogram_num_instructors:
            status_check= StatusDateCheck.objects.filter(training_program=editprogram)
            status_check.filter(status="انتظار قبول الطلب من قبل جميع المدربين").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T')
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
        date_time=timezone.now()
        for instructor_id in editprogram.instructorid:
                try:
                    instructor = FacultyStaff.objects.get(id=instructor_id)

                    status_message = f"تم تعديل تفاصيل البرنامج التدريبي {editprogram.topic} من قبل وحدة الأعمال. "

                    new_notification = Notification(
                        faculty_target=instructor,
                        training_program=editprogram,
                        notification_message=status_message,
                        need_to_be_shown=True,
                         

                    )
                    new_notification.save()
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'تعديل برنامج التدريب', status_message)

                except ObjectDoesNotExist:
                    print(f'Faculty_Staff with id {instructor_id} does not exist')
        

        return redirect('business_unit_account:program_view' , program_id = editprogram.programid )

    return render(request, 'bu/TraningProgram-edit.html', {'IdStatusDateAccept':IdStatusDateAccept, 'numofreq_instructors':numofreq_instructors, 'waitingforaccept':waitingforaccept , 'program':editprogram ,'faculty':faculty , 'domain':domain ,  'id_status_dates' : id_status_dates, 'programflow':programflow, 'notifications_in_programs':notifications_in_programs,
                                                           'notifications_in_tasks':notifications_in_tasks})

@login_required
def program_view(request , program_id):
    user = request.user
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())

    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())

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
   
    return render(request, 'bu/TraningProgram-view.html', {'newinstructors':newinstructors, 'numofreq':numofreq  ,'forall':forall,'user':user,'waitingforaccept':waitingforaccept,'IdStatusDateAccept':IdStatusDateAccept, 'program': program ,'id_status_dates': id_status_dates , 'programflow' : programflow , 'applicationidcount':applicationidcount,'IdStatusDateRejectionValues':IdStatusDateRejectionValues, 'IdStatusDateRejection': IdStatusDateRejection , 'faculty_members':faculty_members, 'notifications_in_programs':notifications_in_programs, 'notifications_in_tasks':notifications_in_tasks})

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
def sendtokai(request, programid):
    user = request.user
    if request.method == 'POST':
            KaiEmployee = Kaibuemployee.objects.all()
            program = Trainingprogram.objects.get(programid=programid)

            notifications = Notification.objects.filter(
                training_program=program,
                faculty_target=user,
                function_indicator=1
            )
            print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
            for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()
                notification.refresh_from_db()
                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

            
            new_notification = Notification(
                    training_program=program,
                    notification_message="تم ارسال طلب برنامج تدريبي من قبل وحده الأعمال الرجاء من احد الموظفين  القيام بإجرأت البرنامج",    
                    
                    function_indicator=1, 
                    target_indicator=2, 
                    need_to_be_shown=True,
                )
            new_notification.save()
            notification_message="تم ارسال طلب برنامج تدريبي من قبل وحده الأعمال الرجاء من احد الموظفين  القيام بإجرأت البرنامج", 
                
            for member in KaiEmployee:
                if member.sendnotificationbyemail:
                    send_custom_email(request, member.email, "إجرائات البرنامج التدريبي" , notification_message)
                        

            program.isbuaccepted = True
            program.status= "تم ارسال الطلب إلى المعهد"
            program.isfacultyfound=True
            program.save()
            status_check= StatusDateCheck.objects.filter(training_program=program)
            status_check.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T')
            status_check.filter(status="تم قبول الطلب من قبل المعهد").update(indicator='C')
            status_check.filter(status="تم ارسال الطلب إلى المعهد").update(date=timezone.now().date() , indicator='T')
            date_time=timezone.now()
            new_notification = Notification(
                           
                            training_program=program,
                            notification_message=f"{program.topic} تم ارسال برنامج تدريبي من قبل وحدة الأعمال", 
                            need_to_be_shown=True,
                             

                        )
            for instructor_id in program.instructorid:
                    try:
                        instructor = FacultyStaff.objects.get(id=instructor_id)

                        status_message = f"تم إزسال البرنامج التدريبي {program.topic} إلى معهد الملك عبدالله للبحوث والدراسات الإستشارية . "

                        new_notification = Notification(
                            faculty_target=instructor,
                            training_program=program,
                            notification_message=status_message,
                            need_to_be_shown=True,
                             

                        )
                        new_notification.save()
                        if instructor.sendnotificationbyemail:
                            send_custom_email(request, instructor.email, ' تغير حالة البرنامج إلى تم إزسال الطلب إلى المعهد ', status_message)


                






                    except ObjectDoesNotExist:
                        print(f'Faculty_Staff with id {instructor_id} does not exist')


            
            return redirect('business_unit_account:program_view' , program_id = program.programid)

@login_required
def publish1(request, program_id):
    user = request.user
    program = Trainingprogram.objects.get(programid=program_id)

    notifications = Notification.objects.filter(training_program=program, faculty_target=user, function_indicator=1)
    print("Notifications Found:", notifications.count())

    for notification in notifications:
        notification.isread = True
        notification.isopened = True
        notification.save()
        notification.refresh_from_db()
        print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')
     
    for instructor_id in program.instructorid:
                
                    instructor = FacultyStaff.objects.get(id=instructor_id)

                    status_message = f" تم نشر البرنامج {program.topic} من قبل وحدة الأعمال. "

                    new_notification = Notification(
                        faculty_target=instructor,
                        training_program=program,
                        notification_message= status_message,
                        need_to_be_shown=True,
                         

                    )
                    new_notification.save()
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'تم نشر البرنامج',status_message)


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
        date_time=timezone.now()

        for instructor_id in program.instructorid:
                    try:
                        instructor = FacultyStaff.objects.get(id=instructor_id)

                        status_message = f"تم نشر البرنامج التدريبي {program.topic}. "

                        new_notification = Notification(
                            faculty_target=instructor,
                            training_program=program,
                            notification_message=status_message,
                            need_to_be_shown=True,
                             

                        )
                        new_notification.save()
                        if instructor.sendnotificationbyemail:
                            send_custom_email(request, instructor.email, 'نشر برنامج تدريبي', status_message)


                






                    except ObjectDoesNotExist:
                        print(f'Faculty_Staff with id {instructor_id} does not exist')
        return redirect('business_unit_account:program_view' , program_id = program.programid)

@login_required
@require_POST
def select_program_team(request, program_id):
    user = request.user
    program = get_object_or_404(Trainingprogram, programid=program_id)
    selected_instructors = request.POST.getlist('trainer_selection')
    
    # Update the instructors for the program
    old_set = set(program.instructorid) if program.instructorid else set()
    new_set = set(int(id) for id in selected_instructors)
    program.instructorid = list(old_set.union(new_set))
    program.save()


    # Iterate over the new set of instructors and send notifications
    for instructor_id in new_set:
        instructor = FacultyStaff.objects.get(id=instructor_id)
        
        # Create a Notification for sorting and selecting the program team
        Notification.objects.create(
            faculty_target=instructor,
            training_program=program,
            notification_message=f"تم فرز الطلبات واختيار فريق البرنامج {program.topic}",
            function_indicator=1,
            need_to_be_shown=True,
        )
        
        # Create a Notification for being chosen in the program team
        Notification.objects.create(
            faculty_target=instructor,
            training_program=program,
            notification_message=f"تم اختيارك في فريق برنامج {program.topic}",
            function_indicator=1,
            need_to_be_shown=True,
        )
        
        # Send email notification if enabled
        if instructor.sendnotificationbyemail:
            send_custom_email(
                request,
                instructor.email,
                'فرز الطلبات واختيار فريق البرنامج',
                f"تم فرز الطلبات واختيار فريق البرنامج {program.topic}"
            )

    # Update program status
    program.appourtunityopentoall = False
    program.status = "تم فرز الطلبات واختيار فريق البرنامج"
    program.save()

    # Update status for selected instructors
    update_status = IdStatusDate.objects.filter(training_program=program)
    for instructor_id in selected_instructors:
        update_status.filter(instructor_id=instructor_id).update(status="تم قبول الطلب من قبل المدرب")

    # Update StatusDateCheck records
    status_check = StatusDateCheck.objects.filter(training_program=program_id)
    status_check.filter(status="تم فرز الطلبات واختيار فريق البرنامج").update(indicator='T', date=timezone.now().date())
    status_check.filter(status="تم ارسال الطلب إلى المعهد").update(indicator='C')

    # Fetch and update notifications for the user
    notifications = Notification.objects.filter(
        training_program=program,
        faculty_target=user,
        function_indicator=1
    )
    print("Notifications Found:", notifications.count())
    
    for notification in notifications:
        notification.isread = True
        notification.isopened = True
        notification.save()
        print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

    
    Notification.objects.create(

                        faculty_target=user,
                        training_program=program,
                        notification_message=F"تم فرز و اختيار فريق البرنامج {program.topic} الرجاء ارسال البرنامج لمعهد الملك عبدالله",
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
    if user.sendnotificationbyemail:
                        send_custom_email(request, user.email,  'فرز الطلبات واختيار فريق البرنامج' ,F"تم فرز و اختيار فريق البرنامج {program.topic} الرجاء ارسال البرنامج لمعهد الملك عبدالله")

            

    # Redirect to the program view
    return redirect('business_unit_account:program_view', program_id=program.programid)

# this view in case instructor have rejected
@login_required
def send_to_new_trainee(request, program_id , instructor_id):
    if request.method == 'POST':
        user = request.user
        print('in send_to_new_trainee')
        date_time=timezone.now()
        try:
            # Get the program from the database
            training_program = Trainingprogram.objects.get(programid=program_id)

            notifications = Notification.objects.filter(
                training_program=training_program,
                faculty_target=user,
                function_indicator=1
            )
            print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
            for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()
                notification.refresh_from_db()
                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

          

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
                    
                    instructor_id = int(new_instructors)  # Convert to integer
                    instructor = FacultyStaff.objects.get(id=instructor_id)
                    status_message = f"تم إرسال طلب من قبل وحدة الأعمال للمشاركة في برنامج تدريبي بعنوان {training_program.topic}. الرجاء الدخول إلى البرنامج وتحديد مشاركتك فيه أو عدم مشاركتك فيه."
                    
                    Notification.objects.create(

                        faculty_target=instructor,
                        training_program=training_program,
                        notification_message=status_message,
                         
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'طلب المشاركة في برنامج التدريب', status_message)           
           

                           
            program = training_program
            return redirect('business_unit_account:program_view' , program_id = program.programid)
        except Trainingprogram.DoesNotExist as e:
            print("Training program not found:", e)
            return HttpResponse("Training program not found")
        except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
    return HttpResponse("Unexpected error or GET request")

# this view in case BU what to request instructor/s for a faculty requset
@login_required
def send_to_new_trainees2(request, program_id):
    if request.method == 'POST':
        print('send_to_new_trainees2')
        try:
            user = request.user
            collage_id = user.collageid.collageid
            # Get the program from the database
            training_program = Trainingprogram.objects.get(programid=program_id)
            
            notifications = Notification.objects.filter(
                training_program=training_program,
                faculty_target=user,
                function_indicator=1
            )
            print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
            for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()
                notification.refresh_from_db()
                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

            training_program.status= "انتظار قبول الطلب من قبل جميع المدربين"
            
            # Get the new instructors from the form
            new_instructors = request.POST.getlist('instructor')
            openToAllCheckbox = request.POST.get('openToAllCheckbox')
            faculty = FacultyStaff.objects.filter(collageid=collage_id)

            if openToAllCheckbox:
                print("send to new trainee case 1")
                
                new_notification = Notification(
                    training_program=training_program,
                    notification_message="فرصه للمشاركة في برنامج تدريبي متاحة للجميع ",    
                    need_to_be_opened=True,
                    function_indicator=1, 
                    target_indicator=1, 
                    need_to_be_shown=True,
                )
                new_notification.save()



                Notification.objects.create(

                        faculty_target=user,
                        training_program=training_program,
                        notification_message=F"تم إنشاء برنامج{training_program.topic} وتم فترح الفرصه لجميع اعضاء هيئة التدريس للمشاركة به الرجاء اختيار فريق العمل عند وجدد عدد كاف من المتقدمين ",
                         
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
                if user.sendnotificationbyemail:
                        send_custom_email(request, member.email, "فرصه للمشاركة في برنامج تدريبي متاحة للجميع " ,"فرصه للمشاركة في برنامج تدريبي متاحة للجميع ")

            
                
                for member in faculty:
                    if member.sendnotificationbyemail:
                        send_custom_email(request, member.email, "فرصه للمشاركة في برنامج تدريبي متاحة للجميع ", "فرصه للمشاركة في برنامج تدريبي متاحة للجميع ")
                        
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
                
                return redirect('business_unit_account:program_view', program_id=training_program.programid)

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
            
                    instructor = FacultyStaff.objects.get(id=instructor_id)
                    status_message = f"يتم إرسال طلب من قبل وحدة الأعمال للمشاركة في برنامج تدريبي بعنوان {training_program.topic}. الرجاء الدخول إلى البرنامج وتحديد مشاركتك فيه أو عدم مشاركتك فيه."
                    
                    new_notification = Notification(
                        faculty_target=instructor,
                        training_program=training_program,
                        notification_message=status_message,     
                        need_to_be_opened=True,
                        function_indicator=1,  
                        need_to_be_shown=True,
                    )
                    new_notification.save()
                    if instructor.sendnotificationbyemail:
                        send_custom_email(request, instructor.email, 'طلب المشاركة في برنامج التدريب', status_message)
                        
            program = training_program
            return redirect('business_unit_account:program_view', program_id = program.programid)
        except Trainingprogram.DoesNotExist:
            print("Training program not found:", e)
         
        except Exception as e:
            print("An error occurred:", e)
           
    print("Didn't enter POST request handling")
    return HttpResponse("Unexpected error or GET request")

# this case if BU what to have more instructor  
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
    user = request.user
    program = get_object_or_404(Trainingprogram, programid=program_id)
    program.status = "تم قبول الطلب من قبل وحدة الأعمال"
    program.isbuaccepted=True
    print(program.programid)
    status_message = f"تم قبول طلب انشاء البرنامج {program.topic}. من قبل وحدة الأعمال."

    notifications = Notification.objects.filter(
                training_program=program,
                faculty_target=user,
                function_indicator=1
            )
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()
                notification.refresh_from_db()
                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

                    
    leader= FacultyStaff.objects.get(id=program.programleader)
    Notification.objects.create(

                        faculty_target= leader,
                        training_program=program,
                        notification_message=status_message,
                         
                        
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
    if leader.sendnotificationbyemail:
        send_custom_email(request, leader.email, 'قبول طلب إنشاء البرنامج التدريبي', status_message)  

     
    status_message2 = f"الرجاء تعين فريق البرنامج {program.topic}."

    Notification.objects.create(

                        faculty_target=user,
                        training_program=program,
                        notification_message=status_message2,
                         
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
    if user.sendnotificationbyemail:
        send_custom_email(request, user.email, 'تعين فريق البرنامج', status_message2)           
                    
           


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
    user = request.user
    rejection_reason = request.POST.get('rejectionReason')
    program = get_object_or_404(Trainingprogram, programid=program_id)
    program.status ="تم رفض الطلب من قبل وحدة الأعمال"
    program.rejectionresons=rejection_reason
    program.isbuaccepted=False
    program.dataofburejection=datetime.now().date()
    program.save()
    leader= FacultyStaff.objects.get(id=program.programleader)

    status_message = f"تم قبول طلب انشاء البرنامج {program.topic}. من قبل وحدة الأعمال."

    notifications = Notification.objects.filter(
                training_program=program,
                faculty_target=user,
                function_indicator=1
            )
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()
                notification.refresh_from_db()
                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

                    
                    

    Notification.objects.create(

                        faculty_target=leader,
                        training_program=program,
                        notification_message=status_message,
                         
                        
                        function_indicator=1,
                        need_to_be_shown=True,

                    )
    if leader.sendnotificationbyemail:
        send_custom_email(request, leader.email, 'قبول طلب إنشاء البرنامج التدريبي', status_message)           
           

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

##################### Project ###################

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
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    all_projects = Project.objects.filter(collageid=collage_id).order_by('-OfferingDate')
    started_projects = Project.objects.filter(collageid=collage_id , status= "تم بدء العمل على المشروع").order_by('-OfferingDate')
    Accepted_projects = Project.objects.filter(collageid=collage_id , isAccepted = True).order_by('-OfferingDate')
    notAccepted_projects = Project.objects.filter(collageid=collage_id , isAccepted = False).order_by('-OfferingDate')

  
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

            # 1
            new_StatusDateCheck =StatusDateCheckProject(
                status="إنشاء المشروع",
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck.save()
            # 2
            new_StatusDateCheck2 =StatusDateCheckProject(
                status="فتح الانضمام للمشروع لأعضاء هيئة التدريس ",
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck2.save()
            # 3
            new_StatusDateCheck3 =StatusDateCheckProject(
                status="تم فرز الطلبات واختيار فريق العمل",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck3.save()
            # 4
            new_StatusDateCheck4 =StatusDateCheckProject(
                status="اختيار رئيس الفريق",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck4.save()
            # 5
            new_StatusDateCheck5 =StatusDateCheckProject(
                status="تم بدء العمل على المشروع",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck5.save()
            # 6
            new_StatusDateCheck8 =StatusDateCheckProject(
                status="المراجعة من قبل المعهد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck8.save()
            # 7
            new_StatusDateCheck10 =StatusDateCheckProject(
                status="حالة المشروع بعد الرد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck10.save()
            # 8
            new_StatusDateCheck10 =StatusDateCheckProject(
                status="الانتهاء من المشروع",
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
            # 1
            new_StatusDateCheck =StatusDateCheckProject(
                status="إنشاء المشروع",
                date=timezone.now().date(),
                indicator='T',# means finished
                project=new_project)
            new_StatusDateCheck.save()
            # 2
            new_StatusDateCheck2 =StatusDateCheckProject(
                status=tempStatus,
                date=timezone.now().date(),
                indicator='T',
                project=new_project)
            new_StatusDateCheck2.save()
            # 3
            new_StatusDateCheck3 =StatusDateCheckProject(
                status=tempStatus2,
                date=None,
                indicator='C',
                project=new_project)
            new_StatusDateCheck3.save()
            # 4
            new_StatusDateCheck4 =StatusDateCheckProject(
                status=tempStatus3,
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck4.save()
            # 5
            new_StatusDateCheck5 =StatusDateCheckProject(
                status="اختيار رئيس الفريق",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck5.save()
            # 6
            new_StatusDateCheck6 =StatusDateCheckProject(
                status="تم بدء العمل على المشروع",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck6.save()
            # 7
            new_StatusDateCheck9 =StatusDateCheckProject(
                status="المراجعة من قبل المعهد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck9.save()
            # 8
            new_StatusDateCheck11 =StatusDateCheckProject(
                status="حالة المشروع بعد الرد",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck11.save()
            # 9
            new_StatusDateCheck10 =StatusDateCheckProject(
                status="الانتهاء من المشروع",
                date=None,
                indicator='W',
                project=new_project)
            new_StatusDateCheck10.save()

            print("case 2")
            return redirect('business_unit_account:projects')

    return render(request, 'bu/Projects.html', {'user': user , 'faculty':faculty, 'all_projects':all_projects ,'started_projects':started_projects,'Accepted_projects':Accepted_projects,'notAccepted_projects':notAccepted_projects})

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
        editproject.save()

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
        IdStatusDateAccept = IdStatusDate.objects.filter(project=editproject, status= "تم قبول الطلب من قبل العضو").count()
        editprogram_num_team= int(editproject.num_ofTeam)
        status_check= StatusDateCheckProject.objects.filter(project=editproject)
        checkStartproject = status_check.get(status="تم بدء العمل على المشروع")

        if status_check.filter(status="انتظار قبول الطلب من قبل جميع الفريق") : 
            checkWaiting = status_check.get(status="انتظار قبول الطلب من قبل جميع الفريق")
            if IdStatusDateAccept == editprogram_num_team  and  checkWaiting.indicator != 'T' :
                print('here')
                status_check.filter(status="انتظار قبول الطلب من قبل جميع الفريق").update(indicator='T')
                # status_check.filter(status="تم قبول الطلب من قبل العضو").update(indicator='T')
                status_check.filter(status="تم قبول الطلب من قبل جميع الفريق").update(indicator='T')

                checkleader = status_check.get(status="اختيار رئيس الفريق")
                if checkleader.indicator == 'W' :
                    print('here2')
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

            elif IdStatusDateAccept == editprogram_num_team and checkStartproject.indicator != 'T':
                status_check.filter(status="تم بدء العمل على المشروع").update(indicator='T', date=timezone.now().date())
                status_check.filter(status='تم قبول الطلب من قبل جميع الفريق').update(indicator='T')
                editproject.status = "تم بدء العمل على المشروع"

        editproject.save()

        bu = FacultyStaff.objects.get(collageid=user.collageid , is_buhead=True)
        url = f"https://api.chatengine.io/chats/{editproject.chatgroup_id}/"
        payload = {"title": editproject.Name }
        headers = {
            'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
            'User-Name': bu.username,
            'User-Secret': str(bu.id),
        }
        response = requests.request("PATCH", url, headers=headers, data=payload)
        print(response.text)
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
    TeamAcceptance = IdStatusDate.objects.filter( project=program_id, status= "تم قبول الطلب من قبل العضو")
    faculty_members = FacultyStaff.objects.filter(collageid=project.collageid)
    numofreq = IdStatusDateAccept + waitingforaccept
    newinstructors = project.num_ofTeam - numofreq 
   
    return render(request, 'bu/Projects-view.html', { 'TeamAcceptance': TeamAcceptance , 'applicationidcount':applicationidcount , 'newinstructors':newinstructors, 'numofreq':numofreq  ,'forall':forall,'user':user,'waitingforaccept':waitingforaccept,'IdStatusDateAccept':IdStatusDateAccept, 'program': project ,'id_status_dates': id_status_dates , 'programflow' : programflow,'IdStatusDateRejectionValues':IdStatusDateRejectionValues, 'IdStatusDateRejection': IdStatusDateRejection , 'faculty_members':faculty_members, 'files':file})

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
    status_check.filter(status="تم بدء العمل على المشروع").update(indicator='T', date=timezone.now().date())
 
    return redirect('business_unit_account:project_view' , program_id = program.programid)

# send to new member after someone reject
@login_required
def send_to_new_member(request, program_id , instructor_id):
    if request.method == 'POST':
        try:
            ('here in send_to_new_member')
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
            status_check.filter(status="تم بدء العمل على المشروع").update(indicator='T', date=timezone.now().date())
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

@login_required
def ConfirmKAI(request, program_id , ConfirmKAI):
    try:
        project = Project.objects.get(programid=program_id)
        status_check= StatusDateCheckProject.objects.filter(project=project)
        if ConfirmKAI == 'true':
            project.isAccepted =True
            project.status = "تم تعميد المشروع"
        elif ConfirmKAI == 'false':
            project.isAccepted = False
            project.status = "لم يتم تعميد المشروع"
            status_check.filter(status="الانتهاء من المشروع").update(indicator='T',date = date.today())
        project.save()

        status_check.filter(status="حالة المشروع بعد الرد").update(indicator='T',date = date.today())
        print('project', project.isAccepted)
        return redirect('business_unit_account:project_view' , program_id = project.programid)
    except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
    except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")
    
@login_required
def SubmittedtoKAI(request, program_id):
    try:
        project = Project.objects.get(programid=program_id)
        project.isSubmittedtoKAI =True
        status_check= StatusDateCheckProject.objects.filter(project=project)
        status_check.filter(status="المراجعة من قبل المعهد").update(indicator='T',date = date.today())
        project.status = "تتم المراجعة من قبل المعهد"
        project.save()
        print('project', project.isSubmittedtoKAI)
        return redirect('business_unit_account:project_view' , program_id = project.programid)
    except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
    except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")

def ConfirmDONEproject(request, program_id):
    try:
        project = Project.objects.get(programid=program_id)
        status_check= StatusDateCheckProject.objects.filter(project=project)
        status_check.filter(status="الانتهاء من المشروع").update(indicator='T',date = date.today())
        project.status = "تم الانتهاء من المشروع"
        project.save()
        print('project', project.isSubmittedtoKAI)
        return redirect('business_unit_account:project_view' , program_id = project.programid)
    except Project.DoesNotExist as e:
            print("Project not found:", e)
            return HttpResponse("Project not found")
    except Exception as e:
            print("An error occurred:", e)
            return HttpResponse("An error occurred")

###################### Task ############################

from django.db.models import Q, Case, When, IntegerField

@login_required
def task_view(request):
    user = request.user
    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
        )
    
    userFaculty = get_object_or_404(FacultyStaff, id=user.id)
    collage_id = user.collageid.collageid
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    allCollages = Collage.objects.all()
    kaiBuHead= Kaibuemployee.objects.filter(position="رئيس قسم وحدات الأعمال")
    otherCollagesBUHeads = FacultyStaff.objects.filter(is_buhead=True).exclude(collageid=collage_id)
    collageDean = FacultyStaff.objects.filter(position='عميد الكلية', collageid=collage_id)    
    allFaculties=FacultyStaff.objects.all()
    allKaiEmployees=Kaibuemployee.objects.all()

    LATE = 'متأخرة'
    URGENT = 'عاجلة'
    COMPLETED = 'منجزة'
    RETRIEVED = 'مسترجعة'

    sort_priority = Case(
    When(Q(status=LATE) & Q(priority=URGENT), then=0),  # Late and urgent
    When(~Q(status=COMPLETED) & ~Q(status=RETRIEVED), then=1),  # All other statuses except completed or retrieved
    When(Q(status=COMPLETED) | Q(status=RETRIEVED), then=2),  # Completed or retrieved
    output_field=IntegerField()
    )

    allTasksAssignedByUser = Task.objects.filter(
    faculty_initiation=user.id
    ).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
     )
    
    allTasksAssignedToUser = Task.objects.filter(faculty_ids__contains=[int(user.id)]).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
    )
    all_tasks_related_to_user = Task.objects.filter(Q(faculty_initiation=user.id) | Q(faculty_ids__contains=[int(user.id)])).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
    )
    all_tasks_related_to_user_that_ended = Task.objects.filter(Q(status='منجزة') & (Q(faculty_initiation=user.id) | Q(faculty_ids__contains=[int(user.id)])))
    
    assigned_by_user_task_ids = allTasksAssignedByUser.values_list('task_id', flat=True)
    assigned_to_user_task_ids = allTasksAssignedToUser.values_list('task_id', flat=True)
    related_ended_user_task_ids = all_tasks_related_to_user_that_ended.values_list('task_id', flat=True)

    combined_tasks_ids = notifications_in_tasks.values_list(
                  'taskid__task_id', flat=True).distinct()

# Initialize lists to hold categorized notifications
    notifications_in_assigned_by_user_tasks = []
    notifications_in_assigned_to_user_tasks = []
    notifications_in_related_ended_user_tasks = []

# Iterate over notifications to categorize them
    for notification in notifications_in_tasks:
        task_id = notification.taskid.task_id  # Assuming taskid is a ForeignKey to Task and the related name is 'id'
        if task_id in assigned_by_user_task_ids:
            notifications_in_assigned_by_user_tasks.append(notification)
        elif task_id in assigned_to_user_task_ids:
            notifications_in_assigned_to_user_tasks.append(notification)
        elif task_id in related_ended_user_task_ids:
            notifications_in_related_ended_user_tasks.append(notification)

# Now you can work with the categorized lists of notifications
# For example, to print the count of notifications in each category:
        print('a')
        print(len(notifications_in_assigned_by_user_tasks))
        print('b')
        print(len(notifications_in_assigned_to_user_tasks))
        print('c')
        print(len(notifications_in_related_ended_user_tasks))

    notifications_in_assigned_by_user_tasks_count = len(notifications_in_assigned_by_user_tasks)
    notifications_in_assigned_to_user_tasks_count = len(notifications_in_assigned_to_user_tasks)
    notifications_in_related_ended_user_tasks_count = len(notifications_in_related_ended_user_tasks)
    

    if request.method == 'POST':
        tasktype = request.POST.get('tasktype')
        tasktopic = request.POST.get('tasktopic')
        taskdescription = request.POST.get('taskdescription')
        isclassifide = request.POST.get('isclassifide')
        notes = request.POST.get('notes')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        kai_ids = []
        faculty_ids = []
        full_accomplishment = request.POST.get('isfull_accomplishment')

        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = None
            attachment_name = ''
        requiredprocedure = request.POST.get('requiredprocedure')
        priority = request.POST.get('priority')
        assiningto = request.POST.getlist('assiningto')
        ToAll = False

        for assign in assiningto:
            if assign.startswith('a.'):
                kai_id = assign.split('.')[1]
                kai_ids.append(kai_id)
            elif assign.startswith('b.'):
                ToAll = True
            elif assign.startswith('c.'):
                faculty_id = assign.split('.')[1]
                faculty_ids.append(faculty_id)
            elif assign.startswith('d.'):
                faculty_id = assign.split('.')[1]
                faculty_ids.append(faculty_id)
        
        tempStatus = ''
        tempStatus2=''
        if ToAll == True:
            tempStatus = '''تم ارسال المهمة إلى موظفين
معهد الملك عبدالله للبحوث
و الدراسات الإستشارية'''
            tempStatus2='KAi مرسله إلى موظفين ال '
        elif kai_ids:
            tempStatus = 'تم إسناد المهمة'
            tempStatus2='مسندة'
        else:
            tempStatus = 'تم إسناد المهمة'
            tempStatus2='مسندة'
        

        print(tasktype, tasktopic,taskdescription, isclassifide, notes, priority , assiningto, startdate, enddate)

        new_task = Task(
           task_name = tasktopic,
           task_type = tasktype,
           task_description = taskdescription,
           is_classified = isclassifide,
           start_date = startdate,
           end_date = enddate,
           notes = notes,
           necessary_procedure = requiredprocedure,
           priority = priority,
           faculty_initiation = userFaculty,
           faculty_ids= faculty_ids,
           kai_ids =  kai_ids ,
           status=tempStatus2,
           is_main_task = True,
           attachment = attachment,
           toall=ToAll,
           full_accomplishment = full_accomplishment 

        )
        new_task.save()

       
        status_message_notfy = f"تم اسناد مهمة {new_task.task_name} إليك الرجاء إنجاز المهمة"
        body = f'''\
        السلام عليكم،

        نود إعلامكم بأن مهمة جديدة بعنوان {new_task.task_name} قد تم تكليفها إليكم. نأمل منكم البدء في تنفيذ المهمة وفقاً للمتطلبات المحددة.

        نشكركم مقدماً على جهودكم ونتطلع إلى إنجازكم لهذا العمل بالجودة والكفاءة المعهودة.

        مع خالص التقدير والاحترام,

        بوابة الأعمال
        '''

        for id in kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)

            new_notification = Notification(
            kaitarget=instructor,
            taskid=new_task,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)
        
        for id in faculty_ids:
            instructor =FacultyStaff.objects.get(id=id)

            new_notification = Notification(
            faculty_target=instructor,
            taskid=new_task,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)



        print("KAI IDs before saving:", kai_ids)
        print("Faculty IDs before saving:", faculty_ids)
        print("KAI IDs after saving:", new_task.kai_ids)
        print("Faculty IDs after saving:", new_task.faculty_ids)
        print(len(new_task.kai_ids))
        print(len(new_task.faculty_ids))
        
        status_message = f"تم إنشاء المهمة من قبل {user.first_name} {user.last_name}"
        new_task.statusarray.append(status_message)
        new_task.statusarray.append(tempStatus)

        today = timezone.localdate()
        new_task.datearray.append(today)
        new_task.datearray.append(today)

        new_task.save()
        date_time=timezone.now() 

        for id in new_task.faculty_ids:
            faculty = FacultyStaff.objects.get(pk = id)

            new_taskToUser = TaskToUser(
                main_task=new_task,
                faculty_user = faculty,
                status='مسندة',
                date_time=date_time,

            )
            new_taskToUser.save()
        
        for id in new_task.kai_ids:
            kaiuser = Kaibuemployee.objects.get(pk = id)
            new_taskToUser = TaskToUser(
                main_task=new_task,
                kai_user=kaiuser,
                status='مسندة',
                date_time=date_time,

            )
            new_taskToUser.save()
        return redirect('business_unit_account:tasks')
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())

    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())
    current_date = timezone.now().date()
    
    all_notifications_that_needs_to_be_shown = Notification.objects.filter(faculty_target=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        faculty_target=user, 
        need_to_be_shown=True,
        isread=False
    ).count()

    return render(request, 'bu/Tasks.html', {'faculty':faculty,'user': user, 'allCollages':allCollages, 'kaiBuHead':kaiBuHead, 'otherCollagesBUHeads':otherCollagesBUHeads, 'collageDean':collageDean, 'allTasksAssignedByUser':allTasksAssignedByUser, 'allTasksAssignedToUser':allTasksAssignedToUser, 'all_tasks_related_to_user':all_tasks_related_to_user, 'allFaculties':allFaculties, 'allKaiEmployees':allKaiEmployees, 'all_tasks_related_to_user_that_ended':all_tasks_related_to_user_that_ended , 'notifications_in_programs':notifications_in_programs, 'notifications_in_tasks':notifications_in_tasks, 'notifications_in_assigned_by_user_tasks':notifications_in_assigned_by_user_tasks_count, 'notifications_in_assigned_to_user_tasks':notifications_in_assigned_to_user_tasks_count, 'notifications_in_related_ended_user_tasks':notifications_in_related_ended_user_tasks_count, 'combined_tasks_ids':combined_tasks_ids, 'current_date':current_date, 'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown,'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count})

@login_required
def task_details(request, task_id):
    
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    print(f"Task ID: {task_id}, Pending Status: {givenTask.pending_status}")
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )

    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())
    

    pending_requestor_names = []
    if givenTask.pending_rquestids is not None:
        for user_id_modified in givenTask.pending_rquestids:
            try:
        # Split the user_id_modified by period and unpack into prefix and user_id
                prefix, user_id = user_id_modified.split('.')
            except ValueError:
        # Log the error or handle it as needed
                print(f"Error: user_id_modified '{user_id_modified}' is not in the expected format.")
                continue  # Skip this iteration and continue with the next

            if prefix == 'b':
                try:
            # Query the Kaibuemployee table
                    inPending = Kaibuemployee.objects.get(pk=user_id)
                except Kaibuemployee.DoesNotExist:
            # Handle the case where the Kaibuemployee does not exist
                    print(f"Kaibuemployee with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            elif prefix == 'a':
                try:
            # Query the FacultyStaff table
                    inPending = FacultyStaff.objects.get(pk=user_id)
                except FacultyStaff.DoesNotExist:
            # Handle the case where the FacultyStaff does not exist
                    print(f"FacultyStaff with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            else:
        # Handle unexpected prefix or error
                print(f"Unexpected prefix {prefix}.")
                continue  # Skip this iteration and continue with the next

            if inPending:
                pending_requestor_names.append(f"{inPending.first_name} {inPending.last_name}")
        
    
    print(notifications_in_programs.count())
    collage_id = user.collageid.collageid
    
    allCollages = Collage.objects.all()
    kaiBuHead= Kaibuemployee.objects.filter(position="رئيس قسم وحدات الأعمال")
    otherCollagesBUHeads = FacultyStaff.objects.filter(is_buhead=True).exclude(collageid=collage_id)
    collageDean = FacultyStaff.objects.filter(position='عميد الكلية', collageid=collage_id)
    faculty_user = TaskToUser.objects.filter(main_task_id=task_id).values_list('faculty_user', flat=True)
    kai_user = TaskToUser.objects.filter(main_task_id=task_id).values_list('kai_user', flat=True)

    rejected_tasks = TaskToUser.objects.filter(
    main_task=task_id,
    status='مرفوضة'
    ).order_by('-date_time')
    number_of_tasks_to_retrieve = givenTask.countrejection
    recent_rejected_tasks = rejected_tasks[:number_of_tasks_to_retrieve]



    Faculty_user = None
    Kai_user = None
    if givenTask.faculty_ids and len(givenTask.faculty_ids) > 0:
        Faculty_user = FacultyStaff.objects.filter(pk__in=givenTask.faculty_ids)
    if givenTask.kai_ids and len(givenTask.kai_ids) > 0:
        Kai_user = Kaibuemployee.objects.filter(pk__in=givenTask.kai_ids)
    

    userAssignment = TaskToUser.objects.filter(main_task_id=task_id, faculty_user=user, status='مسندة').count()
    userAccompleshment = TaskToUser.objects.filter(main_task_id=task_id, faculty_user=user, status='منجزة').count()
    userrejection = TaskToUser.objects.filter(main_task_id=task_id, faculty_user=user, status='مرفوضة').count()



    faculty_objects = FacultyStaff.objects.filter(id__in=faculty_user)
    Kai_objects = Kaibuemployee.objects.filter(id__in=kai_user)
    task_hierarchy = build_task_hierarchy(givenTask)

    
    NotCompletedSubTasks= Task.objects.filter(
    Q(main_task=givenTask) & Q(faculty_initiation=user) & (Q(status='مسندة') | Q(status='KAi مرسله إلى موظفين ال '))
)
   

    not_completed_subtasks_count = Task.objects.filter(
    Q(main_task=givenTask) & Q(faculty_initiation=user) & (Q(status='مسندة') | Q(status='KAi مرسله إلى موظفين ال '))
).count()
    


    

    def flatten_hierarchy(task, hierarchy, result=None):
        if result is None:
            result = []

        result.append((task, hierarchy[task]['level']))
        for subtask in hierarchy[task]['subtasks']:
            flatten_hierarchy(subtask, hierarchy, result)

        return result

    # Flatten the hierarchy
    flat_hierarchy = flatten_hierarchy(givenTask, task_hierarchy)
    
    
    
    
    if request.method == 'POST':
        tasktype = request.POST.get('tasktype')
        tasktopic = request.POST.get('tasktopic')
        taskdescription = request.POST.get('taskdescription')
        isclassifide = request.POST.get('isclassifide')
        notes = request.POST.get('notes')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        kai_ids = []
        faculty_ids = []
        full_accomplishment = request.POST.get('isfull_accomplishment')
        
        


       
        
        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = None
            attachment_name = ''
        requiredprocedure = request.POST.get('requiredprocedure')
        priority = request.POST.get('priority')
        assiningto = request.POST.getlist('assiningto')
        ToAll = False
        print(assiningto)

        for assign in assiningto:
            if assign.startswith('a.'):
                kai_id = assign.split('.')[1]
                kai_ids.append(kai_id)
                print('kai',kai_id)
            elif assign.startswith('b.'):
                ToAll = True
            elif assign.startswith('c.'):
                faculty_id = assign.split('.')[1]
                faculty_ids.append(faculty_id)
                print('faculty',faculty_id)
            elif assign.startswith('d.'):
                faculty_id = assign.split('.')[1]
                faculty_ids.append(faculty_id)
                print('faculty',faculty_id)
        
        tempStatus = ''
        tempStatus2=''
        if ToAll == True:
            tempStatus = '''تم ارسال المهمة الفرعية إلى موظفين
معهد الملك عبدالله للبحوث
و الدراسات الإستشارية'''
            tempStatus2='KAi مرسله إلى موظفين ال '
        elif kai_ids:
            tempStatus = 'تم إسناد المهمة الفرعية'
            tempStatus2='مسندة'
        else:
            tempStatus = 'تم إسناد المهمة الفرعية'
            tempStatus2='مسندة'
        

        print(tasktype, tasktopic,taskdescription, isclassifide, notes, priority , assiningto, startdate, enddate)
        print("hi")




        new_task = Task(
           task_name = tasktopic,
           task_type = tasktype,
           task_description = taskdescription,
           is_classified = isclassifide,
           start_date = startdate,
           end_date = enddate,
           notes = notes,
           necessary_procedure = requiredprocedure,
           priority = priority,
           faculty_initiation = user,
           faculty_ids= faculty_ids,
           kai_ids =  kai_ids ,
           status=tempStatus2,
           is_main_task = False,
           attachment = attachment,
           main_task=givenTask,
           toall=ToAll,
           full_accomplishment=full_accomplishment

        )
        new_task.save()

        status_message_notfy = f"تم اسناد مهمة {new_task.task_name} إليك الرجاء إنجاز المهمة"

        body = f'''\
        السلام عليكم،

        نود إعلامكم بأن مهمة جديدة بعنوان {new_task.task_name}  قد تم تكليفها إليكم. نأمل منكم البدء في تنفيذ المهمة وفقاً للمتطلبات المحددة.  

        نشكركم مقدماً على جهودكم ونتطلع إلى إنجازكم لهذا العمل بالجودة والكفاءة المعهودة.

        مع خالص التقدير والاحترام,

        بوابة الأعمال
        '''

        for id in kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)

            new_notification = Notification(
            kaitarget=instructor,
            taskid=new_task,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)
        
        for id in faculty_ids:
            instructor =FacultyStaff.objects.get(id=id)

            new_notification = Notification(
            faculty_target=instructor,
            taskid=new_task,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)

        print("KAI IDs before saving:", kai_ids)
        print("Faculty IDs before saving:", faculty_ids)
        print("KAI IDs after saving:", new_task.kai_ids)
        print("Faculty IDs after saving:", new_task.faculty_ids)

        status_message = f"تم إنشاء المهمة الفرعية من قبل {user.first_name} {user.last_name}"
        new_task.statusarray.append(status_message)
        new_task.statusarray.append(tempStatus)

        today = timezone.localdate()
        new_task.datearray.append(today)
        new_task.datearray.append(today)

        new_task.save()
        date_time=timezone.now() 

        for id in new_task.faculty_ids:
            faculty = FacultyStaff.objects.get(pk = id)

            new_taskToUser = TaskToUser(
                main_task=new_task,
                faculty_user = faculty,
                status='مسندة',
                date_time=date_time,

            )
            new_taskToUser.save()
            print('facultyTaskToUser')
        
        for id in new_task.kai_ids:
            kaiuser = Kaibuemployee.objects.get(pk = id)
            new_taskToUser = TaskToUser(
                main_task=new_task,
                kai_user=kaiuser,
                status='مسندة',
                date_time=date_time,

            )
            new_taskToUser.save()
            print('facultyTaskToUser')



        



        return redirect('business_unit_account:task-detail', task_id=task_id)






    pending_reasons = givenTask.pending_reasons if givenTask.pending_reasons is not None else []
    status_with_dates = zip(givenTask.datearray, givenTask.statusarray)
    zipped_names_reasons = zip(pending_requestor_names, pending_reasons)
    current_date = timezone.now().date()

    all_notifications_that_needs_to_be_shown = Notification.objects.filter(faculty_target=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        faculty_target=user, 
        need_to_be_shown=True,
        isread=False
    ).count()

    # Now pass the modified givenTask to your template context
    return render(request, 'bu/Task_view.html', {
        'givenTask': givenTask,
        'allCollages': allCollages,
        'kaiBuHead': kaiBuHead,
        'otherCollagesBUHeads': otherCollagesBUHeads,
        'collageDean': collageDean,
        'faculty_objects': faculty_objects,
        'kai_objects': Kai_objects,
        'NotCompletedSubTasks': NotCompletedSubTasks,
        'not_completed_subtasks_count': not_completed_subtasks_count,
        'status_with_dates': status_with_dates,
        'flat_hierarchy': flat_hierarchy,
        'Faculty_user':Faculty_user,
        'Kai_user':Kai_user,
        'userAssignment':userAssignment,
        'userAccompleshment':userAccompleshment,
        'userrejection':userrejection,
        'recent_rejected_tasks':recent_rejected_tasks,
        'notifications_in_programs':notifications_in_programs,
        'pending_requestor_names':pending_requestor_names,
        'zipped_names_reasons': zipped_names_reasons,
        'notifications_in_tasks':notifications_in_tasks,
        'current_date':current_date,
        'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown,
        'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count,



    })

from collections import OrderedDict

def build_task_hierarchy(task, hierarchy=None, level=0):
    if hierarchy is None:
        hierarchy = {}
    
    # Get subtasks for the current task
    subtasks = Task.objects.filter(main_task=task)
    
    # Add the current task to the hierarchy
    hierarchy[task] = {"level": level, "subtasks": []}
    
    # Iterate over subtasks and recursively build the hierarchy
    for subtask in subtasks:
        hierarchy[task]["subtasks"].append(subtask)
        build_task_hierarchy(subtask, hierarchy, level + 1)
    
    return hierarchy


@login_required
def retrieve_task(request, task_id):
    user = request.user

    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_tasks.count())

    
    givenTask = get_object_or_404(Task, pk=task_id)
    allSubTaskes = Task.objects.filter(main_task=task_id)
    tempCount = allSubTaskes.count()
    today = timezone.localdate()
    date_time=timezone.now() 

    notifications = Notification.objects.filter(
            taskid=givenTask,
            
                
                
            )
    for notification in notifications:
        notification.need_to_be_opened=False
        notification.isread = True
        notification.save()

    print("Notifications Found:", notifications.count())

    status_message_notfy=f"تم استرجاع المهمة {givenTask.task_name}"

    body = f'''\
    إشعار بتحديث حالة المهمة

    السلام عليكم،

    نود إعلامكم بأنه قد تم استرجاع المهمة {givenTask.task_name} ولم تعد مكلفين بها. نأمل التأكد من تحديث أولويات العمل الخاصة بكم وفقًا لهذا التغيير. 

    نشكركم على جهودكم ونتطلع إلى تعاونكم في المهام القادمة.

    لديكم أي استفسارات أو تحتاجون إلى مزيد من المعلومات، يرجى التواصل معنا.

    مع خالص التقدير والاحترام,
    
    بوابة الأعمال

    '''

   


    for id in givenTask.kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)

            new_notification = Notification(
            kaitarget=instructor,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'إسترجاع المهمة', body)
        
    for id in givenTask.faculty_ids :
            instructor =FacultyStaff.objects.get(id=id)

            new_notification = Notification(
            faculty_target=instructor,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)


    AllTaskToUser = TaskToUser.objects.filter(main_task=task_id)
    for subTask in AllTaskToUser:
        subTask.status ='مسترجعة'
        subTask.addeddate= today
        subTask.date_time=date_time
        subTask.save()
    

    for task in allSubTaskes:
        print("Inside subtask loop")
        task.status = 'مسترجعة'
        task.retrivalDate= today
        task.kai_ids.clear()
        task.faculty_ids.clear()

        status_message = f"تم إسترجاع المهمة الفرعية من قبل {user.first_name} {user.last_name}"

        task.statusarray.append(status_message)
        task.datearray.append(today)
        task.save()
        date_time=timezone.now()
        AllTaskToUser = TaskToUser.objects.filter(main_task=task.task_id)
        for subTask in AllTaskToUser:
            subTask.status ='مسترجعة'
            subTask.addeddate= today
            subTask.date_time=date_time
            subTask.save()

    givenTask.status='مسترجعة'
    givenTask.save()


    
    if tempCount > 0:
        status_message = f" تم إسترجاع جميع المهام التابعة قبل {user.first_name} {user.last_name}"
        givenTask.statusarray.append(status_message)
        givenTask.datearray.append(today)



    status_message = f" تم إسترجاع المهمة قبل {user.first_name} {user.last_name}"
    
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.retrivalDate= today
    
    givenTask.kai_ids.clear()
    givenTask.faculty_ids.clear()
    givenTask.save()
    return redirect('business_unit_account:tasks')


@login_required
def reject_task(request, task_id):
    user = request.user
    tasktouser =TaskToUser.objects.filter(main_task=task_id, faculty_user=user)
    reason=''
    if request.method == 'POST':
        reason = request.POST.get('rejection_reasons')
       
    givenTask = get_object_or_404(Task, pk=task_id)
    notifications = Notification.objects.filter(
                taskid=givenTask,
                faculty_target=user,
                need_to_be_opened=True,
              
            )
    
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')


    status_message_notfy = f"تم رفض المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name} الرجاء اعادة اسناد المهمةاو حلها"
    body = f'''\
    إشعار برفض المهمة

    السلام عليكم،

    نود إحاطتكم علمًا بأن المهمة بعنوان {givenTask.task_name}  قد تم رفضها من قبل  {user.first_name} {user.last_name}. نرجو من الجهة المعنية إعادة تكليف المهمة لشخص آخر أو العمل على حلها. 

    نشكركم على تعاونكم ونتطلع إلى معالجة هذا الأمر بأسرع وقت ممكن.

    بوابة الأعمال

    
    '''
    if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
        new_notification = Notification(
            faculty_target=givenTask.faculty_initiation ,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
        new_notification.save()
        if givenTask.faculty_initiation.sendnotificationbyemail:
                send_custom_email(request, givenTask.faculty_initiation .email, 'رفض المهمة', body)
        
        
    if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
        
        new_notification = Notification(
            kaitarget=givenTask.kai_initiation,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            need_to_be_opened=True,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
        new_notification.save()
        if givenTask.kai_initiation.sendnotificationbyemail:
                send_custom_email(request, givenTask.kai_initiation.email, 'رفض المهمة', body)
        
        

    givenTask.faculty_ids.remove(int(user.id))
    today = timezone.localdate()
  
    
    if len(givenTask.kai_ids) == 0 and len(givenTask.faculty_ids) == 0:
        givenTask.status = 'مرفوضة'
        print('T1')
        givenTask.save()
    else:
        if givenTask.status == 'منجزة جزئياً' or givenTask.status == 'منجزة جزئياً، مرفوضة من البعض':
            givenTask.status = 'منجزة جزئياً، مرفوضة من البعض'
            givenTask.save()
            print('T2')
        else:
            givenTask.status = 'تم الرفض من قبل البعض'
            givenTask.save()
            print('T3')
    
    status_message = f" تم رفض المهمة من قبل {user.first_name} {user.last_name}"
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.countrejection+=1
    givenTask.save()
    date_time=timezone.now()
    for task in tasktouser:
            if task.status == 'مسندة':
                task.status = 'مرفوضة'
                task.addeddate= today
                task.addedtext= reason
                task.date_time=date_time
                task.save()

    return redirect('business_unit_account:tasks')
    

@login_required
def Task_completion(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    notifications = Notification.objects.filter(
                taskid=givenTask,
                faculty_target=user,
                need_to_be_opened=True,
              
            )
    
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')


   
        

    notcompletedtasks = TaskToUser.objects.filter(main_task=task_id, status='مسندة')
    countnotcompletedtasks = notcompletedtasks.count()
    today = timezone.localdate()
    status_message=''
    taskdescription=''
    attachment=None
    if request.method == 'POST':
        taskdescription = request.POST.get('taskdescription')
        if 'attachment' in request.FILES:
            attachment = request.FILES['attachment'].read()
            attachment_name = request.FILES['attachment'].name
        else:
            attachment = None
            attachment_name = ''
        

    tasktouserid =TaskToUser.objects.filter(main_task=task_id, faculty_user=user)
    today = timezone.localdate()
    date_time=timezone.now() 
    
    for task in tasktouserid:
        if task.status != 'مرفوضة':
            task.status = 'منجزة'
            task.addeddate= today
            task.date_time=date_time
            task.addedtext=taskdescription
            task.attachment=attachment
            task.save()
    
    if givenTask.full_accomplishment:
        if countnotcompletedtasks-1 > 0 or givenTask.countrejection > 0:
            status_message = f" تم إنجاز جزئياً المهمة من قبل {user.first_name} {user.last_name}"
            body = f'''\
            إشعار بإنجاز جزئي للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة قد تم إنجازها جزئيًا من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.

           لأية أسئلة أو مساعدة إضافية، يرجى التواصل مع فريق الدعم.

           مع أطيب التحيات,

    
        '''
            givenTask.status = 'منجزة جزئياً'
            givenTask.save()

            status_message_notfy=f" تم إنجاز جزئياً المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
         

            if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة جزئياً', body)
        
        
            if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', body)
        
        



            if givenTask.countrejection: 
                givenTask.status = 'منجزة جزئياً، مرفوضة من البعض'
                givenTask.save()

        else:
            status_message = f" تم إنجاز المهمة من قبل {user.first_name} {user.last_name}"
            givenTask.status = 'منجزة'
            givenTask.save()
            status_message_notfy=f" تم إنجاز جزئياً المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
            body = f'''\
            إشعار بإنجاز جزئي للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة قد تم إنجازها جزئيًا من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.

           لأية أسئلة أو مساعدة إضافية، يرجى التواصل مع فريق الدعم.

           مع أطيب التحيات,

    
        '''
         

            if  hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة جزئياً', body)
        
        
            if  hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
                
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', body)
            
            status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
            body = f'''\
            إشعار بإنجاز  للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة قد تم إنجازها  من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.

           لأية أسئلة أو مساعدة إضافية، يرجى التواصل مع فريق الدعم.

           مع أطيب التحيات,

    
           '''
         

            if  hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation.email, ' إنجاز المهمة ', body)
        
        
            if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', body)
        
        
        
    else:

        status_message = f"  تم إنجاز المهمة من قبل {user.first_name} {user.last_name}"  
        body = f'''\
            إشعار بإنجاز  للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة قد تم إنجازها  من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.

           لأية أسئلة أو مساعدة إضافية، يرجى التواصل مع فريق الدعم.

           مع أطيب التحيات,

    
           '''
        givenTask.status = 'منجزة'
        givenTask.save()

        status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
         

        if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة ', body)
        
        
        if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة ', body)
        for id in givenTask.kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)
            new_notification = Notification(
                     faculty_target=instructor ,
                  
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                    send_custom_email(request, instructor.email, ' إنجاز المهمة ', body)

        for id in givenTask.faculty_ids :
            
            instructor =FacultyStaff.objects.get(id=id)
            new_notification = Notification(
                     faculty_target=instructor,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                    send_custom_email(request, instructor.email, ' إنجاز المهمة ', body)

        

    today = timezone.localdate()
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.save()
    print(len(givenTask.kai_ids))
    print(len(givenTask.kai_ids))
    
    return redirect('business_unit_account:tasks')

@login_required
def MainTask_completion(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    tasktouser =TaskToUser.objects.filter(main_task=task_id, faculty_user=user)
    givenTask.status ='منتهية'
    givenTask.save()
    for task in tasktouser:
            if task.status == 'مسندة':
        
                task.status = 'منتهية'
                task.save()
    today = timezone.localdate()
    status_message = f"{user.first_name} {user.last_name}إنهاءالمهمة من قبل"
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('business_unit_account:tasks')

@login_required
@require_POST
def ask_for_pending(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)


    status_message_notfy=f"طلب تعليق المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
         

    if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                   need_to_be_opened=True,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, 'طلب تعليق المهمة', status_message_notfy)
        
        
    if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     need_to_be_opened=True,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email,'طلب تعليق المهمة', status_message_notfy)
        
        



    pending_reasons = request.POST.get('pending_reasons')

    # Initialize as lists if they are None
    if givenTask.pending_reasons is None:
        givenTask.pending_reasons = []
    if givenTask.pending_rquestids is None:
        givenTask.pending_rquestids = []

    # Modify the user ID and append to the lists if pending_reasons is provided
    if pending_reasons:
        user_id_modified = 'a.' + str(user.id)
        givenTask.pending_reasons.append(pending_reasons)
        givenTask.pending_rquestids.append(user_id_modified)

    # Set the pending status and status message
    givenTask.pending_status = 'طلب تعليق المهمة'
    status_message = f"طلب تعليق المهمة من قبل {user.first_name} {user.last_name}"
    today = timezone.localdate()

    # Ensure `statusarray` and `datearray` are initialized as lists if they are None
    if givenTask.statusarray is None:
        givenTask.statusarray = []
    if givenTask.datearray is None:
        givenTask.datearray = []

    # Append the status message and today's date to the respective lists
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(str(today))  # Convert today to string if necessary

    # Save the task with all the appended information
    givenTask.save()

    return redirect('business_unit_account:tasks')  # Replace with your actual redirect destination

@login_required
def accepte_pending_request(request, task_id):
    print("in accepte_pending_request")
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    notifications = Notification.objects.filter(
                taskid=givenTask,
                faculty_target=user,
                need_to_be_opened=True,
              
            )
    
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()
            

    status_message_notfy=f"تم قبول طلب تعليق المهمة {givenTask.task_name}"
    
    pending_requestor_names = []
    if givenTask.pending_rquestids is not None:
        for user_id_modified in givenTask.pending_rquestids:
            try:
        # Split the user_id_modified by period and unpack into prefix and user_id
                prefix, user_id = user_id_modified.split('.')
            except ValueError:
        # Log the error or handle it as needed
                print(f"Error: user_id_modified '{user_id_modified}' is not in the expected format.")
                continue  # Skip this iteration and continue with the next

            if prefix == 'b':
                try:
            # Query the Kaibuemployee table
                    inPending = Kaibuemployee.objects.get(pk=user_id)

                    new_notification = Notification(
                          kaitarget= inPending,
                          taskid=givenTask,
                          notification_message=status_message_notfy,
                          
                         
            
                         function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                         need_to_be_shown=True,

                    )
                    new_notification.save()
                    if inPending.sendnotificationbyemail:
                        send_custom_email(request, inPending.email,'قبول تعليق المهمة', status_message_notfy)
    

                except Kaibuemployee.DoesNotExist:
            # Handle the case where the Kaibuemployee does not exist
                    print(f"Kaibuemployee with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            elif prefix == 'a':
                try:
            # Query the FacultyStaff table
                    inPending = FacultyStaff.objects.get(pk=user_id)
                    new_notification = Notification(
                          faculty_target= inPending,
                          taskid=givenTask,
                          notification_message=status_message_notfy,
                         
                         
            
                         function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                         need_to_be_shown=True,

                    )
                    new_notification.save()
                    if inPending.sendnotificationbyemail:
                        send_custom_email(request, inPending.email,'قبول تعليق المهمة', status_message_notfy)
                except FacultyStaff.DoesNotExist:
            # Handle the case where the FacultyStaff does not exist
                    print(f"FacultyStaff with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            else:
        # Handle unexpected prefix or error
                print(f"Unexpected prefix {prefix}.")
                continue  # Skip this iteration and continue with the next

            if inPending:
                pending_requestor_names.append(f"{inPending.first_name} {inPending.last_name}")
        






    givenTask.pending_status='مهمة معلقة'
    status_message = f" تم قبول تعليق المهمة من قبل {user.first_name} {user.last_name} "
    givenTask.statusarray.append(status_message)
    today = timezone.localdate()
    givenTask.datearray.append(today)


    givenTask.save()
    print('pending status: ' + givenTask.pending_status)
    return redirect('business_unit_account:tasks')

@login_required
def reject_pending_request(request, task_id):
    print("in reject_pending_request")
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    notifications = Notification.objects.filter(
                taskid=givenTask,
                faculty_target=user,
                need_to_be_opened=True,
              
            )
    
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

   

    status_message_notfy=f"تم رفض تعليق المهمة {givenTask.task_name}"
    pending_requestor_names = []
    if givenTask.pending_rquestids is not None:
        for user_id_modified in givenTask.pending_rquestids:
            try:
        # Split the user_id_modified by period and unpack into prefix and user_id
                prefix, user_id = user_id_modified.split('.')
            except ValueError:
        # Log the error or handle it as needed
                print(f"Error: user_id_modified '{user_id_modified}' is not in the expected format.")
                continue  # Skip this iteration and continue with the next

            if prefix == 'b':
                try:
            # Query the Kaibuemployee table
                    inPending = Kaibuemployee.objects.get(pk=user_id)

                    new_notification = Notification(
                          kaitarget= inPending,
                          taskid=givenTask,
                          notification_message=status_message_notfy,
                          
                         
            
                         function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                         need_to_be_shown=True,

                    )
                    new_notification.save()
                    if givenTask.inPending.sendnotificationbyemail:
                        send_custom_email(request, givenTask.inPending.email,'رفض تعليق المهمة', status_message_notfy)
    

                except Kaibuemployee.DoesNotExist:
            # Handle the case where the Kaibuemployee does not exist
                    print(f"Kaibuemployee with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            elif prefix == 'a':
                try:
            # Query the FacultyStaff table
                    inPending = FacultyStaff.objects.get(pk=user_id)
                    new_notification = Notification(
                          faculty_target= inPending,
                          taskid=givenTask,
                          notification_message=status_message_notfy,
                         
                         
            
                         function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                         need_to_be_shown=True,

                    )
                    new_notification.save()
                    if givenTask.inPending.sendnotificationbyemail:
                        send_custom_email(request, givenTask.inPending.email,'رفض تعليق المهمة', status_message_notfy)
                except FacultyStaff.DoesNotExist:
            # Handle the case where the FacultyStaff does not exist
                    print(f"FacultyStaff with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            else:
        # Handle unexpected prefix or error
                print(f"Unexpected prefix {prefix}.")
                continue  # Skip this iteration and continue with the next

            if inPending:
                pending_requestor_names.append(f"{inPending.first_name} {inPending.last_name}")
        



    givenTask.pending_status='رفض المهمة المعلقة'
    status_message = f" تم رفض تعليق المهمة من قبل {user.first_name} {user.last_name} "
    givenTask.statusarray.append(status_message)
    today = timezone.localdate()
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('business_unit_account:tasks')

@login_required
def editTask(request, task_id):
    user = request.user
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    print(notifications_in_programs.count())
    givenTask = get_object_or_404(Task, pk=task_id)

    status_message_notfy=f" تم تعديل تفاصيل البرنامج{givenTask.task_name}"

   


    '''for id in givenTask.kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)

            new_notification = Notification(
            kaitarget=instructor,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'تعديل تفاصيل البرنامج', status_message_notfy)'''
        
    '''for id in givenTask.faculty_ids :
            instructor =FacultyStaff.objects.get(id=id)

            new_notification = Notification(
            faculty_target=instructor,
            taskid=givenTask,
            notification_message=status_message_notfy,
                         
            
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,

            )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'تعديل تفاصيل البرنامج', status_message_notfy)'''


    notifications_in_tasks = Notification.objects.filter(
        faculty_target=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    all_notifications_that_needs_to_be_shown = Notification.objects.filter(faculty_target=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        faculty_target=user, 
        need_to_be_shown=True,
        isread=False
    ).count()


    context = {
        'task': givenTask,
        'notifications_in_programs':notifications_in_programs,
        'notifications_in_tasks':notifications_in_tasks,
        'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown,'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count


        # Include other context variables here as needed
    }

    

    if request.method == 'POST':

    # Get the updated form data
        givenTask.task_description = request.POST['taskdescription'] 
        givenTask.start_date = request.POST['startdate']
        givenTask.end_date = request.POST['enddate']
        givenTask.save()
        status_message = f" تم تعديل تفاصيل المهمة من قبل {user.first_name} {user.last_name} "
        givenTask.statusarray.append(status_message)
        today = timezone.localdate()
        givenTask.datearray.append(today)
        

    # Correct usage of render
    return render(request, 'bu/Task_edit.html', context)

###################### End of Task ############################

@login_required
def send_to_new_Instructor(request, task_id ):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    givenTask.countrejection = 0
    givenTask.save()

    notifications = Notification.objects.filter(
                taskid=givenTask,
                faculty_target=user,
                need_to_be_opened=True,
              
            )
    
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()


    notcompletedtasks = TaskToUser.objects.filter(main_task=task_id, status='مسندة')
    countnotcompletedtasks = notcompletedtasks.count()

    if request.method == 'POST':
        checkbox_clicked = 'no-assignment' in request.POST
        if checkbox_clicked:


            if givenTask.status =='منجزة جزئياً، مرفوضة من البعض' or givenTask.status == 'منجزة جزئياً':
                if countnotcompletedtasks>0:
                    givenTask.status =  'منجزة جزئياً'

                    status_message = f"تم حل وضع المهمة المرفوضة بواسطة {user.first_name} {user.last_name}"
                    givenTask.statusarray.append(status_message)
                    today = timezone.localdate()
                    givenTask.datearray.append(today)
                    givenTask.save()
                else:
                    givenTask.status='منجزة'

                    status_message = f"تم حل وضع المهمة المرفوضة بواسطة {user.first_name} {user.last_name}"
                    givenTask.statusarray.append(status_message)
                    today = timezone.localdate()
                    givenTask.datearray.append(today)
                    givenTask.save()
            if givenTask.status == 'تم الرفض من قبل البعض':
                givenTask.status='مسندة'

                status_message = f"تم حل وضع المهمة المرفوضة بواسطة {user.first_name} {user.last_name}"
                givenTask.statusarray.append(status_message)
                today = timezone.localdate()
                givenTask.datearray.append(today)
                givenTask.save()

            


            if givenTask.status=='مرفوضة':

                givenTask.status='مسترجعة'
                status_message = f" تم إسترجاع المهمة قبل {user.first_name} {user.last_name}"
                givenTask.statusarray.append(status_message)
                today = timezone.localdate()
                givenTask.datearray.append(today)
                givenTask.save()
    
        else:
            
        
            assiningto = request.POST.getlist('assigningto')
            ToAll = False
            kai_ids=[]
            faculty_ids=[]

            for assign in assiningto:
                if assign.startswith('a.'):
                    kai_id = assign.split('.')[1]
                    if kai_id not in givenTask.kai_ids:
                        givenTask.kai_ids.append(kai_id)
                        kai_ids.append(kai_id)
                elif assign.startswith('b.'):
                    ToAll = True
                elif assign.startswith('c.'):
                    faculty_id = assign.split('.')[1]
                    if faculty_id not in givenTask.faculty_ids:
                        givenTask.faculty_ids.append(faculty_id)
                        faculty_ids.append(faculty_id)
                elif assign.startswith('d.'):
                    faculty_id = assign.split('.')[1]
                    if faculty_id not in givenTask.faculty_ids:
                        givenTask.faculty_ids.append(faculty_id)
                        faculty_ids.append(faculty_id)
        
            tempStatus = ''
            tempStatus2=''
            if ToAll == True:
                tempStatus = '''تم ارسال المهمة  إلى موظفين
معهد الملك عبدالله للبحوث
و الدراسات الإستشارية'''
                tempStatus2='KAi مرسله إلى موظفين ال '
            elif kai_ids:
                tempStatus = 'تم إعادة إسناد المهمة '
                tempStatus2='مسندة'
            else:
                tempStatus = 'تم إعادة إسناد المهمة '
                tempStatus2='مسندة'

        
            for id in faculty_ids:
                faculty = FacultyStaff.objects.get(pk = id)
                allTaskToUserByFacultyAndGivenTask= TaskToUser.objects.filter(main_task_id=task_id, faculty_user=faculty)
                allTaskToUserByFacultyAndGivenTask.delete()

                new_taskToUser = TaskToUser(
                    main_task=givenTask,
                    faculty_user = faculty,
                    status='مسندة'

                )
                new_taskToUser.save()
                print('facultyTaskToUser')
                status_message_notfy = f"تم اسناد مهمة {givenTask.task_name} إليك الرجاء إنجاز المهمة"

                new_notification = Notification(
                faculty_target=faculty,
                taskid=givenTask,
                notification_message=status_message_notfy,
                         
                
                function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                need_to_be_opened=True,

                )
                new_notification.save()

                
        
            for id in kai_ids:
                kaiuser = Kaibuemployee.objects.get(pk = id)
                allTaskToUserByKAIUserAndGivenTask= TaskToUser.objects.filter(main_task_id=task_id, kai_user=kaiuser)
                allTaskToUserByKAIUserAndGivenTask.delete()
                new_taskToUser = TaskToUser(
                    main_task=givenTask,
                    kai_user=kaiuser,
                    status='مسندة',

                )
                new_taskToUser.save()
                
                status_message_notfy = f"تم اسناد مهمة {givenTask.task_name} إليك الرجاء إنجاز المهمة"

                new_notification = Notification(
                kaitarget=kaiuser,
                taskid=givenTask,
                notification_message=status_message_notfy,
                         
                
                function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                need_to_be_opened=True,

                )
                new_notification.save()
                new_notification.save()
                if kaiuser.sendnotificationbyemail:
                    send_custom_email(request, kaiuser.email, 'مهمة مسندة', status_message)


            if givenTask.status =='منجزة جزئياً، مرفوضة من البعض':
                givenTask.status =  'منجزة جزئياً'
            else:
                givenTask.status = tempStatus2
        
            givenTask.statusarray.append(tempStatus)
            today = timezone.localdate()
            givenTask.datearray.append(today)
            givenTask.save()
    return redirect('business_unit_account:tasks')

###################### Email #####################

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.http import HttpResponse
import certifi

def send_custom_email(request, receiver_email, topic, message):   
           
    subject = topic
    body = message

    # Create MIMEText object with the body text and charset
    body_mime = MIMEText(body, 'plain', 'utf-8')

    # Construct the email with headers and body
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = settings.EMAIL_HOST_USER
    email_msg['To'] = receiver_email  # Set the receiver's email address
    email_msg.attach(body_mime)

    # Create the SSL context for a secure connection
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Connect to the SMTP server, secure the connection, login, and send the email
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as connection:
            connection.starttls(context=ssl_context)  # Secure the connection with TLS
            connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Perform SMTP authentication
            connection.sendmail(settings.EMAIL_HOST_USER, [receiver_email], email_msg.as_string())  # Send the email to the receiver
        print("Email sent successfully to", receiver_email)
        return HttpResponse("Email sent successfully.")
    except smtplib.SMTPException as e:
        print("Error: unable to send email", e)
        return HttpResponse("Email could not be sent.", status=500)

########### app heder notification ######################

@login_required
def update_notifications_ajax(request):
    # Retrieve the logged-in user
    user = request.user
    all_notifications_that_needs_to_be_shown = Notification.objects.filter(faculty_target=user, need_to_be_shown=True)

    for totify in all_notifications_that_needs_to_be_shown:
        totify.isread = True
        totify.save()

    return HttpResponse(status=204)

@login_required
def update_notifications_ajax_Delete(request, notification_id):
    # Retrieve the logged-in user
    user = request.user

    givenNotification = get_object_or_404(Notification, id=notification_id)
    givenNotification.need_to_be_shown=False
    givenNotification.save()
    return HttpResponse(status=204)

from django.http import HttpResponseRedirect

def refresh_current_page(request):
    current_url = request.get_full_path()

    # Redirect to the same URL
    return HttpResponseRedirect(current_url)