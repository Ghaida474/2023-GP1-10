import random
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import requests
from app.models import  FacultyStaff,Collage, Trainingprogram,Register,Trainees,IdStatusDate, StatusDateCheck, Project, StatusDateCheckProject,Files, Notification 
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
import mimetypes
from django.views.decorators.http import require_POST
from django.http import FileResponse, Http404, HttpResponse , JsonResponse , HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

################### communication ###################

@login_required
def joinroom_notification(request):
    program_id = request.GET.get('program_id')
    roomID = random.randint(0, 9999)
    project = Project.objects.get(programid=program_id)
    Teamid = project.Teamid
    for member in Teamid:
        if request.user.id != member:
            instructor = FacultyStaff.objects.get(id=member)
            new_notification = Notification(
                faculty_target=instructor,
                project=project,
                notification_message=F"تم بدء اجتماع افتراضي لمشروع {project.Name} للمشاركة، الدخول على الموقع واستخدام رقم الاجتماع {roomID}",
                need_to_be_opened=True,
                function_indicator=1,
                need_to_be_shown=True,
            )
            new_notification.save()
            if instructor.sendNotificationByEmail:
                message = f'''\
                إشعار ببدء اجتماع افتراضي لمشروع 

                السلام عليكم،

                تم بدء اجتماع افتراضي لمشروع  بعنوان {project.Name}

                للمشاركة، الدخول على الموقع واستخدام رقم الاجتماع {roomID}

                لأية أسئلة أو مساعدة إضافية، يرجى التواصل مع فريق الدعم.

                مع أطيب التحيات, '''
                send_custom_email(request, instructor.email, 'طلب المشاركة في برنامج التدريب', message)
    return render(request, 'faculty_staff/videocall.html', {'roomID': roomID, 'name': request.user.first_name + " " + request.user.last_name, 'collageid': request.user.collageid, 'BUhead': request.user.is_buhead, 'id': request.user.id})

@login_required
def videocall(request):
    notifications = viewNotifications(request)
    context = {'name': request.user.first_name + " " + request.user.last_name,'collageid': request.user.collageid, 'BUhead': request.user.is_buhead , 'id':request.user.id}
    context.update(notifications)
    return render(request, 'faculty_staff/videocall.html', context )

@login_required
def joinroom(request):
    notifications = viewNotifications(request)
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/faculty-staff-account/faculty-staff-home/videocall?roomID=" + roomID)
    return render(request, 'faculty_staff/joinroom.html' , notifications)

@login_required
def chat(request):
    username = request.user.username
    secret = request.user.id
    users = filteredUsers(request)
    return render(request, 'faculty_staff/chat.html' , {'username':username , 'secret': secret ,'users':users})

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
    print(mychat)
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
                        if newuser.collageid.collageid == collageidRequest and newuser.position != 'عميد الكلية':
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
    return render(request, 'faculty_staff/chat.html' , context)

################### Profile ###################

@login_required
def calendar(request):
    user = request.user

    # Retrieve projects the user works on
    user_projects = Project.objects.filter(Teamid__contains=[user.id])

    # Retrieve training programs the user works on
    user_training_programs = Trainingprogram.objects.filter(instructorid__contains=[user.id])

    # Combine projects and training programs into a list of events
    tasks = []
    
    #  project 
    for project in user_projects:
       tasks.append({
         'title':"بداية مشروع: "+ project.Name,
           'start': project.OfferingDate.strftime('%Y-%m-%d'),
           
           
     })
       tasks.append({
            'title': "نهاية مشروع: "+ project.Name,
           'start': project.enddate.strftime('%Y-%m-%d')
            
        })
   #  training program 
    for program in user_training_programs:
        tasks.append({
            'title': "بداية برنامج: "+ program.topic,
            'start': program.startdate.strftime('%Y-%m-%d'),
            
        })
        tasks.append({
            'title': "نهاية برنامج: "+ program.topic,
            'start': program.enddate.strftime('%Y-%m-%d'),
            
        })
    context = {'tasks': tasks}
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/calendar.html', context)

@login_required
def viewNotifications(request):
     user = request.user
     notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False,
        )

     notifications_in_projects = Notification.objects.filter(
        faculty_target=user,
        project__isnull=False,
        need_to_be_opened=True,
        isopened=False
        )
     
     notifications_in_programs = notifications_in_programs.values_list('training_program__programid', flat=True).distinct()
     notifications_in_projects = notifications_in_projects.values_list('project__programid', flat=True).distinct()

     all_notifications_that_needs_to_be_shown = Notification.objects.filter(faculty_target=user, need_to_be_shown=True)
     all_notifications_that_needs_to_be_shown_count = Notification.objects.filter( faculty_target=user, need_to_be_shown=True,isread=False ).count()
     
     notifications = { 'notifications_in_programs':notifications_in_programs, 'notifications_in_projects':notifications_in_projects, 'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown, 'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count}
     return notifications

@login_required
def faculty_staff_home (request):
    user = request.user
    if user.new_user:
        return redirect('faculty_staff_account:change_new_user_password')
    else:
        collage_id = user.collageid.collageid
        collage = Collage.objects.get(collageid=collage_id)
        workedOnProjects = IdStatusDate.objects.filter(instructor=user, project__isnull=False ,status ='تم قبول الطلب من قبل العضو').count()
        RejectedProjects = IdStatusDate.objects.filter(instructor=user, project__isnull=False ,status ='تم رفض الطلب من قبل العضو').count()
        workedOnTrainingprogram = IdStatusDate.objects.filter(instructor=user, training_program__isnull=False ,status = "تم قبول الطلب من قبل المدرب").count()
        RejectedTrainingprogram = IdStatusDate.objects.filter(instructor=user, training_program__isnull=False ,status = "تم رفض الطلب من قبل المدرب").count()
        context = { 'user': user, 'collage': collage ,'workedOnProjects':workedOnProjects , 'RejectedProjects':RejectedProjects ,'workedOnTrainingprogram':workedOnTrainingprogram , 'RejectedTrainingprogram':RejectedTrainingprogram }
        notifications = viewNotifications(request)
        context.update(notifications)
        return render(request, 'faculty_staff/Home.html', context)

@login_required
def change_new_user_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.new_user = False
        user.save()
        return redirect('faculty_staff_account:faculty_staff_home')
    return render(request, 'faculty_staff/new-use-reset-password.html')

@login_required
def profile_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    context = {'user': user , 'collagename':collagename }
    notifications = viewNotifications(request)
    context.update(notifications)
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
    context =  {'form': form ,'form2':form2, 'user' : user , 'success':success , 'form2updated':form2updated }             
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/edit-profile.html', context)

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
    
    if request.method == 'POST':
        print('here1')
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "تم تغيير كلمة المرور بنجاح.")
            return redirect('faculty_staff_account:profile')
    context = {'user': user, 'form': form  }
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/change-password.html', context)

################### TraningProgram ###################

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
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    bu_programs = Trainingprogram.objects.filter(collageid=collage_id,instructorid__contains=[user.id]).exclude(programleader=user.id)
    faculty_or_staff_programs = Trainingprogram.objects.filter(collageid=collage_id, initiatedby='FacultyOrStaff' , programleader=user.id)
    opent_to_all_programs = Trainingprogram.objects.filter(collageid=collage_id,appourtunityopentoall=True,status='فتح الفرصة للجميع').exclude(programleader=user.id)
    opent_to_all_programs_list = list(opent_to_all_programs)
    bu_programs_list = list(bu_programs)
    combined_programs = opent_to_all_programs_list + bu_programs_list
    # print('combined_programs',combined_programs)

    rejected = IdStatusDate.objects.filter( status= "تم رفض الطلب من قبل المدرب", instructor=user)
    rejected_programs1 = [reject.training_program for reject in rejected]
    rejected_programs2 = Trainingprogram.objects.filter(collageid=collage_id , status ="تم رفض الطلب من قبل وحدة الأعمال" ,programleader=user.id )
    rejected_projects = list(rejected_programs1) + list(rejected_programs2)


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

        new_notification = Notification(
                    training_program=new_program,
                    notification_message= f"طلب إنشاء برنامج من قبل  {user.first_name} {user.last_name} الرجاء الإطلاع على التفاصيل",
                    function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
                    need_to_be_opened=True,
                    need_to_be_shown=True,
                    bu_target = head)
        new_notification.save()
        if collage.sendNotificationByEmail:
                send_custom_email(request, collage.buemail, 'طلب إنشاء برنامج تدريبي', f"طلب إنشاء برنامج من قبل  {user.first_name} {user.last_name} الرجاء الإطلاع على التفاصيل")
        
        new_notification = Notification(
                    training_program=new_program,
                    notification_message= f"تم ارسال طلب البرنامج {new_program.topic}  لوحدة الاعمال",
                    function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
                    need_to_be_opened=True,
                    need_to_be_shown=True,
                    faculty_target = user)
        new_notification.save()
        if collage.sendNotificationByEmail:
                send_custom_email(request, collage.buemail, 'طلب إنشاء برنامج تدريبي', f"طلب إنشاء برنامج من قبل  {user.first_name} {user.last_name} الرجاء الإطلاع على التفاصيل")
        
        return redirect('faculty_staff_account:traning-program')
    

    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        # need_to_be_shown=True,
        isopened=False)
    
    # Get the program IDs from combined_programs
    combined_program_ids = [program.programid for program in combined_programs]
    print('combined_program_ids1',combined_program_ids)
    # Filter notifications for combined_programs
    notifications_in_combined_programs = notifications_in_programs.filter(training_program__programid__in=combined_program_ids)
    print('notifications_in_combined_programs',notifications_in_combined_programs)
    # Retrieve the programid(s) for combined programs
    combined_program_ids = notifications_in_combined_programs.values_list('training_program__programid', flat=True).distinct()
    print('combined_program_ids',combined_program_ids)
    
    # Get the program IDs from combined_programs
    faculty_or_staff_programs_ids = [program.programid for program in faculty_or_staff_programs]
    # Filter notifications for combined_programs
    notifications_in_faculty_or_staff_programs = notifications_in_programs.filter(training_program__programid__in=faculty_or_staff_programs_ids)
    # Retrieve the programid(s) for combined programs
    faculty_or_staff_programs_ids = notifications_in_faculty_or_staff_programs.values_list('training_program__programid', flat=True).distinct()
    print('faculty_or_staff_programs_ids',faculty_or_staff_programs_ids)

    context =  {'rejected_projects':rejected_projects, 'user': user ,'combined_programs':combined_programs, 'programs':programs,'faculty':faculty, 'domain':domain , 'bu_programs':bu_programs ,'faculty_or_staff_programs':faculty_or_staff_programs ,'opent_to_all_programs':opent_to_all_programs , 'notifications_in_programs':notifications_in_programs, 'notifications_in_faculty_or_staff_programs':notifications_in_faculty_or_staff_programs, 'notifications_in_combined_programs':notifications_in_combined_programs , 'combined_program_ids':combined_program_ids , 'faculty_or_staff_programs_ids':faculty_or_staff_programs_ids }
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/TraningPrograms.html', context)

@login_required
def program_view(request , program_id):
    program = get_object_or_404(Trainingprogram, programid=program_id)
    instructors = program.instructorid
    user = request.user
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
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
    applicationidcount = IdStatusDate.objects.filter(status='participationRequest', instructor =user.id ,training_program = program ).count()
    print('applicationidcount' ,applicationidcount)
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

    notifications = Notification.objects.filter(training_program=program, faculty_target=user, function_indicator=1)
    print("Notifications Found:", notifications.count())

    for notification in notifications:
        notification.isread = True
        notification.isopened = True
        notification.save()
        notification.refresh_from_db()
        print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')


    context =  {'userid': user.id ,'program': program , 'id_status_dates': id_status_dates ,'programflow':programflow ,'isfacultyinarray': isfacultyinarray , 'applicationidcount':applicationidcount, 'notifications_in_programs':notifications_in_programs}
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/TraningProgram-view.html', context )

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
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
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
    context = {'program':editprogram ,'faculty':faculty , 'domain':domain ,'id_status_dates':id_status_dates ,'programflow':programflow, 'notifications_in_programs':notifications_in_programs }
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/TraningProgram-edit.html', context )

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
    notifications_in_programs = Notification.objects.filter(
        faculty_target=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
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

    return render(request, 'faculty_staff/TraningPrograms.html', {'user': user , 'programs':programs,'faculty':faculty, 'domain':domain , 'notifications_in_programs':notifications_in_programs})

@login_required
@require_POST
def accept_program(request, id):
    user = request.user
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage =  Collage.objects.get(collageid=user.collageid.collageid)

    date_time=timezone.now() 
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    training_program = id_status_date.training_program

    # Change status of the current IdStatusDate object
    id_status_date.status = "تم قبول الطلب من قبل المدرب"
    id_status_date.date = timezone.now().date()
    id_status_date.save()

    first_name =user.first_name
    last_name =user.last_name


    # Check if all IdStatusDate objects associated with the same training program have been accepted
    id_status_dates2 = IdStatusDate.objects.filter(training_program=training_program)
    total_count = id_status_dates2.count()
    accepted_count = id_status_dates2.filter(status="تم قبول الطلب من قبل المدرب").count()

    if training_program.num_ofinstructors == len(training_program.instructorid):

        status_date_checks = StatusDateCheck.objects.filter(training_program=training_program)
        for instructor_id in training_program.instructorid:
            if not id_status_dates2.filter(instructor=instructor_id).exists() or id_status_dates2.filter(status="تم قبول الطلب من قبل المدرب", instructor=instructor_id).exists():
                continue
            else:
                new_notification = Notification(
                training_program=training_program,
                notification_message= f"قبول المشاركة في البرنامج  من قبل المدرب {first_name} {last_name}",
                function_indicator=1, 
                need_to_be_shown=True,
                need_to_be_opened=True,
                bu_target = head)
                new_notification.save()
                if collage.sendNotificationByEmail:
                    send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في برنامج التدريب', f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}  ")
                break
        
        else:
            if training_program.num_ofinstructors == 1 or training_program.num_ofinstructors =='1':
                    training_program.status = "تم قبول الطلب من قبل المدرب"
                    status_date_checks.filter(status="تم قبول الطلب من قبل المدرب").update(indicator='T')
                    new_notification = Notification(       
                        training_program=training_program,
                        notification_message= f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name} الرجاء ارسال البرنامج الى المعهد",
                        need_to_be_opened=True,
                        function_indicator=1, 
                        need_to_be_shown=True, 
                        bu_target = head)
                    new_notification.save()
                    if collage.sendNotificationByEmail:
                          send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في برنامج التدريب', f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}  ")
            else:
                    training_program.status = "تم قبول الطلب من قبل جميع المدربين"
                    status_date_checks.filter(status="تم قبول الطلب من قبل جميع المدربين").update(indicator='T' , date=timezone.now().date())
                    new_notification = Notification(
                        training_program=training_program,
                        notification_message= f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}",
                        function_indicator=1, 
                        need_to_be_shown=True,
                        need_to_be_opened=True,
                        bu_target = head)
                    new_notification.save()
                    if collage.sendNotificationByEmail:
                        send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في برنامج التدريب', f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}  ")
                    
                    new_notification = Notification(
                        training_program=training_program,
                        notification_message= f"تم قبول الطلب من قبل جميع المدربين في  {training_program.topic} الرجاء ارسال البرنامج الى المعهد",
                        need_to_be_opened=True,
                        function_indicator=1,
                        need_to_be_shown=True,
                        bu_target = head)
                    new_notification.save()
                    if collage.sendNotificationByEmail:
                        send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في برنامج التدريب', f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}  ")
                                    
            status_date_checks.filter(status="تم ارسال الطلب إلى المعهد").update(indicator='C')
            training_program.save()
    else:
            new_notification = Notification(
                training_program=training_program,
                notification_message= f"قبول المشاركة في البرنامج  من قبل المدرب {first_name} {last_name}",
                function_indicator=1, 
                need_to_be_shown=True,
                need_to_be_opened=True,
                bu_target = head)
            new_notification.save()
            if collage.sendNotificationByEmail:
                send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في برنامج التدريب', f"قبول المشاركة في البرنامج {training_program.topic} من قبل المدرب {first_name} {last_name}  ")

    return redirect('faculty_staff_account:program_view' , program_id = training_program.programid )

@login_required
@require_POST
def apply_for_traningprogram(request, id):
    user = request.user
    training_program = get_object_or_404(Trainingprogram, programid=id)
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage =  Collage.objects.get(collageid=user.collageid.collageid)
    first_name =user.first_name
    last_name =user.last_name

    new_notification = Notification(
            training_program=training_program,
            notification_message= f"{first_name} {last_name} {training_program.topic}  تقدم بالطلب للمشاركة بالبرنامج التدريبي",
            function_indicator=1, 
            need_to_be_shown=True,
            bu_target = head,
            need_to_be_opened=True)
    new_notification.save()
    if collage.sendNotificationByEmail:
        send_custom_email(request, collage.buemail, 'طلب المشاركة بالبرنامج التدريبي',f"{first_name} {last_name} {training_program.topic}تقدم بالطلب للمشاركة بالبرنامج التدريبي")


    IdStatusDate.objects.create(
        instructor_id=user.id,
        status="participationRequest",
        date=timezone.now().date(),
        training_program=training_program)
    
    return redirect('faculty_staff_account:traning-program')

@login_required
@require_POST
def reject_program(request, id):
    user = request.user
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage = Collage.objects.get(collageid=head.collageid.collageid)
    first_name =user.first_name
    last_name =user.last_name

    date_time=timezone.now() 
    rejection_reason = request.POST.get('rejectionReason')
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    training_program = id_status_date.training_program
    print("instructors ids prior are :", training_program.instructorid )
    user = request.user

 
    # Change status of the current IdStatusDate object
    id_status_date.status = "تم رفض الطلب من قبل المدرب"
    id_status_date.date = timezone.now().date()
    id_status_date.rejectionresons= rejection_reason
    id_status_date.save()


    new_notification = Notification( 
            training_program=training_program,
            notification_message= f"رفض المشاركة في البرنامج من قبل المدرب {first_name} {last_name} الرجاء تعين مدرب بديل",
            function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_opened=True,
            need_to_be_shown=True,
            bu_target = head)
    new_notification.save()
    if collage.sendNotificationByEmail:
        send_custom_email(request, collage.buemail, 'رفض طلب المشاركة في برنامج التدريب', f"رفض المشاركة في البرنامج {training_program.topic}  من قبل المدرب  {first_name} {last_name}  الرجاء تعين مدرب بديل")

    # Remove instructor's id from the instructorid array in the associated TrainingProgram object
    instructor_id = id_status_date.instructor_id
    training_program.instructorid = [id for id in training_program.instructorid if id != instructor_id]
    training_program.save()

    return redirect('faculty_staff_account:traning-program')

################### Projects ###################

@login_required
def projects_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    faculty = FacultyStaff.objects.get(collageid=collage_id , id = user.id)
    opent_to_all_programs = Project.objects.filter(collageid=collage_id, appourtunityopentoall=True,status='فتح الفرصة للجميع')
    acceptenss = IdStatusDate.objects.filter(status="تم قبول الطلب من قبل العضو" , instructor=faculty)
    waiting = IdStatusDate.objects.filter( status="في انتظار قبول العضو", instructor=faculty)
    rejected = IdStatusDate.objects.filter( status="تم رفض الطلب من قبل العضو", instructor=faculty)
    # طلبات الشاريع
    opent_to_all_programs_list = list(opent_to_all_programs)
    waiting_projects = [accepted.project for accepted in waiting]
    combined_programs = opent_to_all_programs_list + waiting_projects
    # مشاريع حالية
    accepted_projects = [accepted.project for accepted in acceptenss]
    program = StatusDateCheckProject.objects.filter(project__in=accepted_projects ,status= 'الانتهاء من المشروع' , indicator='W')
    accepted_projects = [accepted.project for accepted in program]
    # مشاريع منتيه
    fineshed_projects = Project.objects.filter(collageid=collage_id, Teamid__contains=[user.id])
    program2 = StatusDateCheckProject.objects.filter(project__in=fineshed_projects ,status= 'الانتهاء من المشروع' , indicator='T')
    fineshed_projects = [fineshed.project for fineshed in program2]
    # مشاريع مرفوضه
    rejected_projects = [accepted.project for accepted in rejected]
#  ******************************************************************
    notifications_in_project = Notification.objects.filter(
        faculty_target=user,
        project__isnull=False,
        need_to_be_opened=True,
        isopened=False)
    
    # Get the program IDs from combined_programs
    combined_program_ids = [program.programid for program in combined_programs]
    print('combined_program_ids1' , combined_program_ids)
    # Filter notifications for combined_programs
    notifications_in_combined_programs = notifications_in_project.filter(project__programid__in=combined_program_ids)
    print('notifications_in_combined_programs' , notifications_in_combined_programs)
    # Retrieve the programid(s) for combined programs
    combined_program_ids = notifications_in_combined_programs.values_list('project__programid', flat=True).distinct()
    print('combined_program_ids2' , combined_program_ids)

    # Get the program IDs from combined_programs
    accepted_projects_ids = [program.programid for program in accepted_projects]
    # Filter notifications for combined_programs
    notifications_in_accepted_programs = notifications_in_project.filter(project__programid__in=accepted_projects_ids)
    # Retrieve the programid(s) for combined programs
    accepted_projects_ids = notifications_in_accepted_programs.values_list('project__programid', flat=True).distinct()

    context = {'combined_program_ids':combined_program_ids ,'accepted_projects_ids':accepted_projects_ids, 'user': user , 'rejected_projects':rejected_projects, 'combined_programs':combined_programs,'accepted_projects':accepted_projects,'fineshed_projects':fineshed_projects, 'faculty':faculty }
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/Projects.html', context)

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
def addFiles_project(request, value_to_edit):
    editprogram = Project.objects.get(programid=value_to_edit)
    user = request.user
    collage_id = user.collageid.collageid
    faculty = FacultyStaff.objects.filter(collageid=collage_id)
    collage =  Collage.objects.get(collageid=collage_id)
    domain = collage.domain
    id_status_dates = IdStatusDate.objects.filter(project=editprogram)
    programflow = StatusDateCheckProject.objects.filter(project=editprogram)
    edit_file = Files.objects.filter(project=editprogram)

    if request.method == 'POST':

     attachment_data = []
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
                
     for attachment_data in attachment_data:
               try:
        # Assuming edit_file is a QuerySet, get the individual object
                   edit_file_instance = edit_file.get(attachment_name=attachment_data['name'])

        # Update attributes of the individual object
                   edit_file_instance.attachment = attachment_data['content']
                   edit_file_instance.project = editprogram
                   edit_file_instance.save()
               except edit_file.model.DoesNotExist:
        # If the file doesn't exist, create a new one
                   edit_file_instance = Files(
                    attachment=attachment_data['content'],
                    attachment_name=attachment_data['name'],
                    project=editprogram)
                   edit_file_instance.save()

     return redirect('faculty_staff_account:project_view', program_id = editprogram.programid )
   
    context =  {'program':editprogram ,'faculty':faculty , 'domain':domain ,'id_status_dates':id_status_dates ,'programflow':programflow, 'files':edit_file}
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/Projects-edit.html', context)

@login_required
def project_view(request , program_id):
    program = get_object_or_404(Project, programid=program_id)
    instructors = program.Teamid
    user = request.user
    instructors_id = program.Teamid
    file = Files.objects.filter(project=program_id)
    instructor_names = []
    for instructors in instructors_id:
        try:
            faculty_staff = FacultyStaff.objects.get(id=instructors)
            name = [faculty_staff.first_name +' '+faculty_staff.last_name , faculty_staff.id , faculty_staff.major , faculty_staff.email ]
            instructor_names.append(name)
        except FacultyStaff.DoesNotExist:
            instructor_names.append("")
    program.instructor_names = instructor_names

 
    id_status_dates = IdStatusDate.objects.filter(project=program)
    team_member = IdStatusDate.objects.filter(project=program , instructor = user.id ,status = 'تم قبول الطلب من قبل العضو').count()
    memberHaveRequest = IdStatusDate.objects.filter(project=program , instructor = user.id ,status = 'participationRequest')
    TeamAcceptance = IdStatusDate.objects.filter( project=program_id, status= "تم قبول الطلب من قبل العضو")
    programflow = StatusDateCheckProject.objects.filter(project=program)
    applicationidcount = IdStatusDate.objects.filter(status='participationRequest', instructor= user.id , project=program).count()
    
    if applicationidcount :
        isfacultyinarray = False
    else:
        isfacultyinarray = True
    
    notifications = Notification.objects.filter(project=program, faculty_target=user, function_indicator=1)
    print("Notifications Found:", notifications.count())

    for notification in notifications:
        notification.isread = True
        notification.isopened = True
        notification.save()
        notification.refresh_from_db()
        print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')

    context =  {'memberHaveRequest': memberHaveRequest ,'TeamAcceptance': TeamAcceptance ,'team_member':team_member ,'userid':user.id ,'program':program , 'id_status_dates': id_status_dates ,'programflow':programflow ,'isfacultyinarray': isfacultyinarray , 'applicationidcount':applicationidcount, 'files': file}
    notifications = viewNotifications(request)
    context.update(notifications)
    return render(request, 'faculty_staff/Projects-view.html', context)

@login_required
@require_POST
def accept_project(request, id): 
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    program = id_status_date.project
    user = id_status_date.instructor
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage =  Collage.objects.get(collageid=user.collageid.collageid)


    id_status_date.status = "تم قبول الطلب من قبل العضو"
    id_status_date.date = timezone.now().date()
    id_status_date.save()

    id_status_dates2 = IdStatusDate.objects.filter(project=program)
    total_count = id_status_dates2.count()
    accepted_count = id_status_dates2.filter(status="تم قبول الطلب من قبل العضو").count()

    status_date_checks = StatusDateCheckProject.objects.filter(project=program)
    checkstart = status_date_checks.get(status="تم بدء العمل على المشروع")

    if program.num_ofTeam == accepted_count and checkstart.indicator != 'T':
        program.status = "تم قبول الطلب من قبل جميع الفريق"
        status_date_checks.filter(status="تم قبول الطلب من قبل جميع الفريق").update(indicator='T' , date=timezone.now().date())

        new_notification = Notification(
            project=program,
            notification_message= f"قبول المشاركة في المشروع {program.Name} من قبل العضو {user.first_name} {user.last_name}",
            function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,
            bu_target = head,
            need_to_be_opened=True)
        new_notification.save()
        if collage.sendNotificationByEmail:
            send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في المشروع', f"قبول المشاركة في المشروع {program.Name} من قبل العضو {user.first_name} {user.last_name}  ")
                    
        new_notification = Notification(
            project=program,
            notification_message= f"تم قبول الطلب من قبل جميع الفريق",
            need_to_be_opened=True,
            function_indicator=1, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,
            bu_target = head)
        new_notification.save()
        if collage.sendNotificationByEmail:
            send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في المشروع', f"قبول المشاركة في المشروع {program.Name} من قبل العضو {user.first_name} {user.last_name}  ")
                               
    else:
        new_notification = Notification(
                project=program,
                notification_message= f"قبول المشاركة في المشروع من قبل العضو  {user.first_name} {user.last_name}",
                function_indicator=1, 
                need_to_be_shown=True,
                bu_target = head,
                need_to_be_opened=True)
        new_notification.save()
        if collage.sendNotificationByEmail:
            send_custom_email(request, collage.buemail, 'قبول طلب المشاركة في المشروع', f"قبول المشاركة في المشروع {program.Name} من قبل العضو {user.first_name} {user.last_name}  ")

         
    checkAccept = status_date_checks.get(status="تم قبول الطلب من قبل جميع الفريق")
    checkleader = status_date_checks.get(status="اختيار رئيس الفريق")

    if(checkstart.indicator == 'T'):
        addmembertogroupchat(request, user , program)
    elif (checkAccept.indicator == 'T' and checkleader == 'W'):
        status_date_checks.filter(status="اختيار رئيس الفريق").update(indicator='C')

    program.save()
    return redirect('faculty_staff_account:project_view' , program_id = program.programid )

@login_required
@require_POST
def apply_for_project(request, id):
    user = request.user
    program = get_object_or_404(Project, programid=id)
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage =  Collage.objects.get(collageid=user.collageid.collageid)


    IdStatusDate.objects.create(
                instructor_id=user.id,
                status="participationRequest",
                date=timezone.now().date(),
                project=program)
    
    new_notification = Notification(
            project=program,
            notification_message= f" {user.first_name} {user.last_name}  {program.Name} تقدم بالطلب للمشاركة في المشروع",
            function_indicator=1, 
            need_to_be_shown=True,
            bu_target = head,
            need_to_be_opened=True)
    new_notification.save()
    if collage.sendNotificationByEmail:
        send_custom_email(request, collage.buemail, 'طلب المشاركة بالبرنامج التدريبي',f"{user.first_name} {user.last_name} {program.Name} تقدم بالطلب  تقدم بالطلب للمشاركة في المشروع")


    return redirect('faculty_staff_account:projects')

@login_required
@require_POST
def reject_project(request, id):
    user = request.user
    rejection_reason = request.POST.get('rejectionReason')
    id_status_date = get_object_or_404(IdStatusDate, id=id)
    program = id_status_date.project
    head=FacultyStaff.objects.get(is_buhead=True, collageid=user.collageid)
    collage = Collage.objects.get(collageid=head.collageid.collageid)
    first_name =user.first_name
    last_name =user.last_name
    print("instructors ids prior are :", program.Teamid )


    # Change status of the current IdStatusDate object
    id_status_date.status = "تم رفض الطلب من قبل العضو"
    id_status_date.date = timezone.now().date()
    id_status_date.rejectionresons= rejection_reason
    id_status_date.save()

    new_notification = Notification( 
        project=program,
        notification_message= f"رفض المشاركة في المشروع {program.Name}  من قبل العضو  {first_name} {last_name} الرجاء تعين عضو بديل",
        function_indicator=1,
        need_to_be_opened=True,
        need_to_be_shown=True,
        bu_target = head)
    new_notification.save()
    if collage.sendNotificationByEmail:
        send_custom_email(request, collage.buemail, 'رفض طلب المشاركة في برنامج التدريب', f"رفض المشاركة في البرنامج{program.Name} من قبل المدرب {first_name} {last_name} الرجاء تعين مدرب بديل")


    # Remove instructor's id from the instructorid array in the associated TrainingProgram object
    team_id = id_status_date.instructor_id
    program.Teamid = [id for id in program.Teamid if id != team_id]
    program.save()
    return redirect('faculty_staff_account:projects')

@login_required
def groupchat_view(request, program_id):
    project = Project.objects.get(programid=program_id)
    if project.chatgroup_id:
         chatid = project.chatgroup_id
         access_key = project.chat_access_key
         context = {'chatgroup_id':chatid , 'program_id':program_id ,'username': request.user.username , 'pass' :request.user.id , 'access_key':access_key }
         return render(request, 'faculty_staff/groupchat.html' , context)
    else:
       chat_credentials = creategroupchat(request , project )
       project.chatgroup_id = chat_credentials['chatid']
       project.chat_access_key = chat_credentials['access_key']
       project.save()
       context = {'chatgroup_id':project.chatgroup_id , 'program_id':program_id ,'username': request.user.username , 'pass' :request.user.id , 'access_key': project.chat_access_key }
       return render(request, 'faculty_staff/groupchat.html' , context)

@login_required
def creategroupchat(request , project):

    bu = FacultyStaff.objects.get(collageid=project.collageid , is_buhead=True)
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
        'User-Name': bu.username,
        'User-Secret': str(bu.id),
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print('------------------')
    print(response.text)
    # print(response.json())
    responseINjson = response.json()
    access_key = responseINjson['access_key']
    chatid = responseINjson['id']
    chat_credentials = {'access_key':access_key , 'chatid':chatid}
    print('chat_credentials' ,chat_credentials)
    print('response.status_code' ,response.status_code)
    return chat_credentials 

@login_required
def addmembertogroupchat(request , user , program):
    print('user',user)
    chatid = program.chatgroup_id
    bu = FacultyStaff.objects.get(collageid=user.collageid , is_buhead=True)
    url = f"https://api.chatengine.io/chats/{chatid}/people/"
    print('url' , url)
    payload = {"username": user.username }
    headers = {
    'Project-ID': 'f0e1d373-0995-4a51-a2df-cf314fc0e034',
    'User-Name': bu.username,
    'User-Secret': str(bu.id),
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

################### email ###################

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.http import HttpResponse

def send_custom_email(request, receiver_email, topic, message):
    # Set the email subject and body to the provided topic and message
    subject = topic
    body = message
    receiver_email = '442200922@student.ksu.edu.sa' 
    # Create MIMEText object with the body text and charset
    body_mime = MIMEText(body, 'plain', 'utf-8')

    # Construct the email with headers and body
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = settings.EMAIL_HOST_USER
    email_msg['To'] = receiver_email  # Set the receiver's email address
    email_msg.attach(body_mime)

    # Create the SSL context for a secure connection
    ssl_context = ssl.create_default_context()

    # Connect to the SMTP server, secure the connection, login, and send the email
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as connection:
        connection.starttls(context=ssl_context)  # Secure the connection with TLS
        connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Perform SMTP authentication
        connection.send_message(email_msg)  # Send the email to the receiver

    print("Email sent successfully to", receiver_email)

    # Return an HttpResponse indicating success
    return HttpResponse("Email sent successfully.")

########### app heder notification ######################

@login_required
def update_notifications_ajax(request):
    # Retrieve the logged-in user
    user = request.user
    all_notifications_that_needs_to_be_shown = Notification.objects.filter( faculty_target=user, need_to_be_shown=True)
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
    return HttpResponseRedirect(current_url)

@login_required
def email_notification_settings(request):
    user = request.user
    if request.method == 'POST':
        user_response = request.POST.get('emailNotif')
        if user_response == 'yes':
            print('yes')
            user.sendNotificationByEmail = True
        elif user_response == 'no':
            print('no')
            user.sendNotificationByEmail = False
        user.save()
    return redirect('faculty_staff_account:faculty_staff_home')

