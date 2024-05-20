import mimetypes
from app.models import FacultyStaff,Collage, Notification , Kaibuemployee , Task , TaskToUser
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from app.forms import updateKai,ChangePasswordForm
from django.shortcuts import get_object_or_404
from app.models import FacultyStaff,Collage, Notification , Kaibuemployee , Task , TaskToUser , Project , Trainingprogram , Files
from django.http import Http404, HttpResponse
from datetime import timezone
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.db.models import Case, When, Value, IntegerField
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.http import HttpResponse
import certifi

from django.db.models import Case, When, Value, IntegerField, DateTimeField, CharField
from django.db.models import Q, Case, When, IntegerField
from collections import OrderedDict



@login_required
def videocall(request):
    notifications = viewNotifications(request)
    context = {'name': request.user.first_name + " " + request.user.last_name , 'id':request.user.id}
    context.update(notifications)
    return render(request, 'kai/videocall.html', context)

@login_required
def joinroom(request):
    notifications = viewNotifications(request)
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/head-kai-account/kai-home/videocall?roomID=" + roomID)
    return render(request, 'kai/joinroom.html' , notifications)

@login_required
def chat(request):
    username = request.user.username
    secret = request.user.id
    users = filteredUsers(request)
    return render(request, 'kai/chat.html' , {'username':username , 'secret': secret ,'users':users})

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
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

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
                    if  newuser.position == 'عميد الكلية' or newuser.is_buhead:
                        matching_users.append({'username': checkuser.get('username'), 'secret': checkuser.get('secret'),'first_name':checkuser.get('first_name'),'last_name':checkuser.get('last_name')})
                else:
                    if checkuser['username'] != request.user.id:
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
    return render(request, 'kai/chat.html' , context)

@login_required
def kai_home (request):
    user = request.user
    if user.new_user:
        return redirect('head-kai-account:change_new_user_password')
    
    # ################################ revenue
    collages = Collage.objects.all()
    collage_data = []

    for collage in collages:

        projects = Project.objects.filter(isAccepted=True, collageid=collage.collageid)
        programs = Trainingprogram.objects.filter(iskaiaccepted=True, collageid=collage.collageid)

        project_count = projects.count()
        program_count = programs.count()

        revenueP = 0 

        for project in projects:
            tax = project.taxpercentage * project.totalcost
            kai = project.kaipercentage * project.totalcost
            revenue = project.totalcost - (tax + kai)
            revenueP += revenue

        revenueT = 0 

        for program in programs:
            if program.attendeescount is not None and program.totalcost is not None:
                total = program.attendeescount * program.totalcost
                facultycost = program.num_ofinstructors * (program.enddate - program.startdate).days * program.cost
                tax = program.taxpercentage * total
                kai = program.kaipercentage * total
                revenue = total - (facultycost + tax + kai)
                revenueT += revenue
        
        collage_data.append({
            'collage': collage,
            'project_count': project_count,
            'program_count': program_count,
            'revenue_per_year_p': revenueP,
            'revenue_per_year_t': revenueT,
            'allRevenue':revenueP + revenueT,
        })

    context = {'user': user, 'collage_data': collage_data }
    notifications = viewNotifications(request)
    context.update(notifications)  
    return render(request, 'kai/Home.html', context) 

@login_required
def change_new_user_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.new_user = False
        user.save()
        return redirect('head-kai-account:kai-home')
    return render(request, 'kai/new-use-reset-password.html')

@login_required
def profile_view(request):
    user = request.user
    context = {'user': user}
    notifications = viewNotifications(request)
    context.update(notifications) 
    return render(request, 'kai/profile.html' , context ) 

@login_required
def editprofile_view(request):
    user = request.user
    form = updateKai(instance=user)
    success = False
    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateKai(request.POST, request.FILES, instance=user)   
            if form.is_valid():    
                form.save()
                success = True
    context = {'form': form , 'user' : user , 'success':success}
    notifications = viewNotifications(request)
    context.update(notifications)       
    return render(request, 'kai/edit-profile.html', context )

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
    context = {'form': form , 'user' : user , 'success':success}
    notifications = viewNotifications(request)
    context.update(notifications)     
    return render(request, 'kai/change-password.html', context)

@login_required
def viewNotifications(request):
    user = request.user
    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False)
    
    notifications_in_programs = Notification.objects.filter(
        kaitarget=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False)

    all_notifications_that_needs_to_be_shown = Notification.objects.filter(kaitarget=user, need_to_be_shown=True)
    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(kaitarget=user,  need_to_be_shown=True, isread=False).count()
     
    notifications = {'notifications_in_tasks':notifications_in_tasks, 'notifications_in_programs':notifications_in_programs, 'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown, 'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count}
    return notifications

################ Tasks ###################

def view_tasktfile(request, task_id, file_id):
    file = get_object_or_404(Files, fileid=file_id, taskid=task_id)
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
def task_view(request):
    user = request.user
    current_date = timezone.now()

    allKaistaff = Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.pk)  # Returns a queryset (iterable)
    departmenthead = Kaibuemployee.objects.filter(is_department_head=True)  # Returns a queryset (iterable)
    kaiHead = Kaibuemployee.objects.filter(position='رئيس قسم وحدات الأعمال بمعهد الملك عبدالله')  # Already correct

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    notifications_in_programs = Notification.objects.filter(
        kaitarget=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
        )

    all_notifications_that_needs_to_be_shown = Notification.objects.filter(kaitarget=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        kaitarget=user, 
        need_to_be_shown=True,
        isread=False
        ).count()
    
    LATE = 'متأخرة'
    URGENT = 'عاجلة'
    COMPLETED = 'منجزة'
    RETRIEVED = 'مسترجعة'

    sort_priority = Case(
    When(Q(status=LATE) & Q(priority=URGENT), then=0),  # Late and urgent
    When(~Q(status=COMPLETED) & ~Q(status=RETRIEVED), then=4),  # All other statuses except completed or retrieved
    When(Q(status=COMPLETED) | Q(status=RETRIEVED), then=5),  # Completed or retrieved
    default=Value(2),
    output_field=IntegerField()
    )

    allTasksAssignedByUser = Task.objects.filter(
    kai_initiation=user.id
    ).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
     )
    allTasksAssignedToUser = Task.objects.filter(kai_ids__contains=[int(user.id)]).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
    )
    all_tasks_related_to_user = Task.objects.filter(Q(kai_initiation=user.id) | Q(kai_ids__contains=[int(user.id)])).annotate(
    sort_priority=sort_priority
    ).order_by(
    'sort_priority', 'end_date'
    )

    #######
    
    all_tasks_related_to_user = Task.objects.filter(Q(kai_initiation=user.id) | Q(kai_ids__contains=[int(user.id)]))
   
    all_tasks_related_to_user_that_ended = Task.objects.filter(Q(status='منجزة') & (Q(kai_initiation=user.id) | Q(kai_ids__contains=[int(user.id)])))
    
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

    userEliment=get_object_or_404(Kaibuemployee, pk=user.id)
    allCollages = Collage.objects.all()
    Dean = Kaibuemployee.objects.filter(position='عميد معهد الملك عبدالله')
    otherCollagesBUHeads = FacultyStaff.objects.filter(is_buhead=True)
    allTasksAssignedByUser = Task.objects.filter(kai_initiation=user.id)
    allTasksAssignedToUser = Task.objects.filter(kai_ids__contains=[user.id])
    all_tasks_related_to_user = Task.objects.filter(Q(kai_initiation=user.id) |  Q(kai_ids__contains=[int(user.id)]))
    allFaculties=FacultyStaff.objects.all()
    allKaiEmployees=Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.id)

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
        full_accomplishment1 = request.POST.get('isfull_accomplishment')
        
        attachment_data = []
        if 'attachment' in request.FILES:
            attachments = request.FILES.getlist('attachment')

            for attachment_file in attachments:
                attachment_data.append({
                    'content': attachment_file.read(),
                    'name': attachment_file.name,
                })

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
            tempStatus = 'تم ارسال المهمة إلى موظفين معهد الملك عبدالله للبحوث و الدراسات الإستشارية'
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
           kai_initiation=userEliment,
           faculty_ids= faculty_ids,
           kai_ids =  kai_ids ,
           status=tempStatus2,
           is_main_task = True,
           #attachment = attachment,
           toall=ToAll,
           full_accomplishment = full_accomplishment1 
        )
        new_task.save()

        if attachment_data:
                for attachmentt in attachment_data:
                    new_file = Files(
                            attachment = attachmentt['content'],
                            attachment_name = attachmentt['name'],
                            taskid = new_task
                    )
                    new_file.save()
         
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
            print( new_notification.need_to_be_shown)
            print("in the loop")
            if instructor.sendNotificationByEmail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)
        
        for id in faculty_ids:
            instructor =FacultyStaff.objects.get(id=id)

            new_notification = Notification(
                bu_target=instructor,
                taskid=new_task,
                notification_message=status_message_notfy,
                function_indicator=2,      
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
            new_notification.save()
            bu_collage = instructor.collageid
            if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, 'مهمة مسندة', body)

        status_message = f"تم إنشاء المهمة من قبل {user.first_name} {user.last_name}"
        new_task.statusarray.append(status_message)
        new_task.statusarray.append(tempStatus)

        today = timezone.localdate()
        new_task.datearray.append(today)
        new_task.datearray.append(today)

        new_task.save()

        for id in new_task.faculty_ids:
            faculty = FacultyStaff.objects.get(pk = id)

            new_taskToUser = TaskToUser(
                main_task=new_task,
                faculty_user = faculty,
                status='مسندة'
            )
            new_taskToUser.save()
        
        for id in new_task.kai_ids:
            kaiuser = Kaibuemployee.objects.get(pk = id)
            new_taskToUser = TaskToUser(
                main_task=new_task,
                kai_user=kaiuser,
                status='مسندة',
            )
            new_taskToUser.save()
        return redirect('head-kai-account:tasks')
    current_date =timezone.now().date()

     ####### these are the correct retrival ####################
    allKaistaff = Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.id)  # Returns a queryset (iterable)
    departmenthead = Kaibuemployee.objects.filter(is_department_head=True).exclude(pk=user.id)
    allKaiEmployees=Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.id)  # Returns a queryset (iterable)
    kaiHead = Kaibuemployee.objects.filter(position='رئيس قسم وحدات الأعمال بمعهد الملك عبدالله').exclude(pk=user.id)  # Already correct
    ####################

    return render(request, 'kai/Tasks.html', {'user': user, 'allCollages':allCollages, 'allTasksAssignedByUser':allTasksAssignedByUser, 'allTasksAssignedToUser':allTasksAssignedToUser, 'all_tasks_related_to_user':all_tasks_related_to_user, 'allFaculties':allFaculties, 'allKaiEmployees':allKaiEmployees, 'otherCollagesBUHeads':otherCollagesBUHeads, 'Dean':Dean, 'notifications_in_tasks':notifications_in_tasks,
                                                    'notifications_in_programs':notifications_in_programs,
                                                    'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown,
                                                    'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count,
                                                     'notifications_in_assigned_by_user_tasks_count': notifications_in_assigned_by_user_tasks_count,
                                                     'notifications_in_assigned_to_user_tasks_count':notifications_in_assigned_to_user_tasks_count,
                                                     'notifications_in_related_ended_user_tasks_count':notifications_in_related_ended_user_tasks_count,
                                                     'notifications_in_assigned_by_user_tasks':notifications_in_assigned_by_user_tasks,
                                                     'notifications_in_assigned_to_user_tasks':notifications_in_assigned_to_user_tasks,
                                                     'notifications_in_related_ended_user_tasks':notifications_in_related_ended_user_tasks,
                                                     'combined_tasks_ids':combined_tasks_ids,
                                                     'current_date':current_date,
                                                      'allKaistaff':allKaistaff, 
                                                      'departmenthead':departmenthead, 
                                                      'kaiHead':kaiHead

                                                     })

@login_required
def task_details(request, task_id):
    user = request.user

    allKaistaff = Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.pk)  # Returns a queryset (iterable)
    departmenthead = Kaibuemployee.objects.filter(is_department_head=True)  # Returns a queryset (iterable)
    kaiHead = Kaibuemployee.objects.filter(position='رئيس قسم وحدات الأعمال بمعهد الملك عبدالله')  # Already correct
    file = Files.objects.filter(taskid=task_id)
    completedTasksByUseres = TaskToUser.objects.filter(main_task=task_id, status = 'منجزة')

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )

    notifications_in_programs = Notification.objects.filter(
        kaitarget=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
        )

    all_notifications_that_needs_to_be_shown = Notification.objects.filter(kaitarget=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        kaitarget=user, 
        need_to_be_shown=True,
        isread=False
        ).count()
    
    givenTask = get_object_or_404(Task, pk=task_id)
    allCollages = Collage.objects.all()

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
    

    rejected_tasks = TaskToUser.objects.filter(
    main_task=task_id,
    status='مرفوضة'
    ).order_by('-date_time')
    number_of_tasks_to_retrieve = givenTask.countrejection
    recent_rejected_tasks = rejected_tasks[:number_of_tasks_to_retrieve]

    otherCollagesBUHeads= FacultyStaff.objects.filter(is_buhead=True)
    allTasksAssignedToUser = Task.objects.filter(faculty_ids__contains=[int(user.id)])
    all_tasks_related_to_user = Task.objects.filter(Q(kai_initiation=user.id) | Q(kai_ids__contains=[int(user.id)]))
    allSubTaskes = Task.objects.filter(main_task=task_id)
    subTasksCount=allSubTaskes.count()
      
    NotCompletedSubTasks= Task.objects.filter(
    (Q(main_task=givenTask) & Q(kai_initiation=user) & Q(status='مسندة')) |( Q(status='KAi مرسله إلى موظفين ال ') & Q(kai_initiation=user))
)
   
    not_completed_subtasks_count = Task.objects.filter(
    (Q(main_task=givenTask) & Q(kai_initiation=user) & (Q(status='مسندة')) | (Q(status='KAi مرسله إلى موظفين ال ')) & Q(kai_initiation=user) )
).count()

    Faculty_user = None
    Kai_user = None
    if givenTask.faculty_ids and len(givenTask.faculty_ids) > 0:
        Faculty_user = FacultyStaff.objects.filter(pk__in=givenTask.faculty_ids)
    if givenTask.kai_ids and len(givenTask.kai_ids) > 0:
        Kai_user = Kaibuemployee.objects.filter(pk__in=givenTask.kai_ids)

    userAssignment = TaskToUser.objects.filter(main_task_id=task_id, kai_user=user, status='مسندة').count()
    userAccompleshment = TaskToUser.objects.filter(main_task_id=task_id, kai_user=user, status='منجزة').count()
    userrejection = TaskToUser.objects.filter(main_task_id=task_id, kai_user=user, status='مرفوضة').count()

    main_task_instance = get_object_or_404(Task, pk=task_id)
    task_hierarchy = build_task_hierarchy(givenTask)

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
        full_accomplishment1 = request.POST.get('isfull_accomplishment')

        

        requiredprocedure = request.POST.get('requiredprocedure')
        priority = request.POST.get('priority')
        assiningto = request.POST.getlist('assiningto')
        ToAll = False

        print(assiningto)

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
                kai_id = assign.split('.')[1]
                kai_ids.append(kai_id)
                
            elif assign.startswith('e.'):
                kai_id = assign.split('.')[1]
                kai_ids.append(kai_id)
        
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
           kai_initiation = user,
           faculty_ids= faculty_ids,
           kai_ids =  kai_ids ,
           status=tempStatus2,
           is_main_task = False,
           #attachment = attachment,
           main_task=main_task_instance,
           toall=ToAll,
           full_accomplishment = full_accomplishment1 

        )
        new_task.save()

        attachment_data = []
        if 'attachment' in request.FILES:
            attachments = request.FILES.getlist('attachment')

            for attachment_file in attachments:
                attachment_data.append({
                    'content': attachment_file.read(),
                    'name': attachment_file.name,
                })
        if attachment_data:
                for attachmentt in attachment_data:
                    new_file = Files(
                            attachment = attachmentt['content'],
                            attachment_name = attachmentt['name'],
                            taskid = new_task
                    )
                    new_file.save()


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
            if instructor.sendNotificationByEmail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', body)
        
        for id in faculty_ids:
            instructor =FacultyStaff.objects.get(id=id)
            
            new_notification = Notification(
                bu_target=instructor,
                taskid=new_task,
                notification_message=status_message_notfy,
                function_indicator=2,     
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
            new_notification.save()
            bu_collage = instructor.collageid
            if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, 'مهمة مسندة', body)

        print(new_task.kai_ids)
        print(new_task.faculty_ids)

        status_message = f"تم إنشاء المهمة الفرعية من قبل {user.first_name} {user.last_name}"
        new_task.statusarray.append(status_message)
        new_task.statusarray.append(tempStatus)

        today = timezone.localdate()
        new_task.datearray.append(today)
        new_task.datearray.append(today)

        new_task.save()

        for id in new_task.faculty_ids:
            faculty = FacultyStaff.objects.get(pk = id)

            new_taskToUser = TaskToUser(
                main_task=new_task,
                faculty_user = faculty,
                status='مسندة'
            )
            new_taskToUser.save()
        
        for id in new_task.kai_ids:
            kaiuser = Kaibuemployee.objects.get(pk = id)
            new_taskToUser = TaskToUser(
                main_task=new_task,
                kai_user=kaiuser,
                status='مسندة',
            )
            new_taskToUser.save()
        return redirect('head-kai-account:task-detail', task_id=task_id)
    
    pending_reasons = givenTask.pending_reasons if givenTask.pending_reasons is not None else []
    status_with_dates = zip(givenTask.datearray, givenTask.statusarray)
    zipped_names_reasons = zip(pending_requestor_names, pending_reasons)
    current_date = timezone.now().date()

     ####### these are the correct retrival ####################
    allKaistaff = Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.id)  # Returns a queryset (iterable)
    departmenthead = Kaibuemployee.objects.filter(is_department_head=True).exclude(pk=user.id)
    allKaiEmployees=Kaibuemployee.objects.filter(is_staff=True).exclude(pk=user.id)  # Returns a queryset (iterable)
    kaiHead = Kaibuemployee.objects.filter(position='رئيس قسم وحدات الأعمال بمعهد الملك عبدالله').exclude(pk=user.id)  # Already correct
    ####################
    return render(request, 'kai/Task_view.html',{'givenTask':givenTask, 'allCollages':allCollages, 'otherCollagesBUHeads':otherCollagesBUHeads,'all_tasks_related_to_user':all_tasks_related_to_user, 'allTasksAssignedToUser':allTasksAssignedToUser, 'subTasksCount':subTasksCount,'NotCompletedSubTasks':NotCompletedSubTasks, 'Faculty_user':Faculty_user, 'Kai_user':Kai_user, 'userAssignment':userAssignment,'userAccompleshment':userAccompleshment, 'userrejection':userrejection, 'pending_requestor_names':pending_requestor_names, 'zipped_names_reasons':zipped_names_reasons, 'status_with_dates':status_with_dates, 'flat_hierarchy':flat_hierarchy, 'not_completed_subtasks_count':not_completed_subtasks_count, 'recent_rejected_tasks':recent_rejected_tasks, 'notifications_in_tasks':notifications_in_tasks, 'current_date':current_date, 'allKaistaff':allKaistaff, 'departmenthead':departmenthead, 'kaiHead':kaiHead, 'completedTasksByUseres':completedTasksByUseres})


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
    givenTask = get_object_or_404(Task, pk=task_id)
    allSubTaskes = Task.objects.filter(main_task=task_id)
    tempCount = allSubTaskes.count()
    today = timezone.localdate()

    notifications = Notification.objects.filter(
            taskid=givenTask, 
            )
    for notification in notifications:
        notification.need_to_be_opened=False
        notification.isread = True
        notification.save()

    kaiids = list(givenTask.kai_ids)
    facultyids = list(givenTask.faculty_ids)

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

    
    AllTaskToUser = TaskToUser.objects.filter(main_task=task_id)
    for subTask in AllTaskToUser:
        subTask.status ='مسترجعة'
        subTask.addeddate= today
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
        AllTaskToUser = TaskToUser.objects.filter(main_task=task.task_id)
        for subTask in AllTaskToUser:
            subTask.status ='مسترجعة'
            subTask.addeddate= today
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

    for id in kaiids:
            instructor = Kaibuemployee.objects.get(id=id)
            print(instructor.first_name)

            new_notification = Notification(
            kaitarget=instructor,
            taskid=givenTask,
            notification_message=status_message_notfy,
            function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,
            )
            new_notification.save()
            if instructor.sendNotificationByEmail:
                send_custom_email(request, instructor.email, 'إسترجاع المهمة', body)
        
    for id in facultyids :
            instructor =FacultyStaff.objects.get(id=id)
            print(instructor.first_name)

            new_notification = Notification(
                bu_target=instructor,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
            new_notification.save()
            bu_collage = instructor.collageid
            if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, 'إسترجاع المهمة', body)
    
    return redirect('head-kai-account:tasks')

@login_required
def reject_task(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    
    body = f'''\
    إشعار برفض المهمة

    السلام عليكم،

    نود إحاطتكم علمًا بأن المهمة بعنوان {givenTask.task_name}  قد تم رفضها من قبل  {user.first_name} {user.last_name}. نرجو من الجهة المعنية إعادة تكليف المهمة لشخص آخر أو العمل على حلها. 

    نشكركم على تعاونكم ونتطلع إلى معالجة هذا الأمر بأسرع وقت ممكن.

    بوابة الأعمال

    
    '''
    
    notifications = Notification.objects.filter(
                taskid=givenTask,
                kaitarget=user,
                need_to_be_opened=True,
            )
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

    status_message_notfy = f"تم رفض المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name} الرجاء اعادة اسناد المهمةاو حلها"
    if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:

        instructor = givenTask.faculty_initiation

        new_notification = Notification(
                bu_target=givenTask.faculty_initiation,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator = 202, 
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
        new_notification.save()
        bu_collage = givenTask.faculty_initiation.collageid
        if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, 'رفض المهمة', body)

    if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:        
        new_notification = Notification(
            kaitarget=givenTask.kai_initiation,
            taskid=givenTask,
            notification_message=status_message_notfy,        
            need_to_be_opened=True,
            function_indicator = 202,  # this is an indicator that will be used when instructor accept or decline a program
            need_to_be_shown=True,
            )
        new_notification.save()
        if givenTask.kai_initiation.sendNotificationByEmail:
                send_custom_email(request, givenTask.kai_initiation.email, 'رفض المهمة', body)
        
    tasktouser =TaskToUser.objects.filter(main_task=task_id, kai_user=user)

    notcompletedtasks_count = TaskToUser.objects.filter(main_task=task_id, status='مسندة').count()

    completedtask_count = TaskToUser.objects.filter(main_task=task_id, status='منجزة').count()
    
    reason=''
    if request.method == 'POST':
        reason = request.POST.get('rejection_reasons')

    givenTask.kai_ids.remove(int(user.id))
    givenTask.save()

    today = timezone.localdate()
    print(len(givenTask.kai_ids))
    print(len(givenTask.kai_ids))

    if len(givenTask.kai_ids) == 0 and len(givenTask.faculty_ids) == 0:
        print('T1')
        givenTask.status = 'مرفوضة'
        givenTask.save()
    else:
        print(givenTask.status)
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

    for task in tasktouser:
            if task.status == 'مسندة':
                task.status = 'رفض المهمة'
                task.addedtext= reason
                task.save()

    return redirect('head-kai-account:tasks')
     
@login_required
def Task_completion(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)

    notifications = Notification.objects.filter(
        taskid=givenTask,
        kaitarget=user,
        need_to_be_opened=True)    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
        notification.isread = True
        notification.isopened = True
        notification.save()
        notification.refresh_from_db()
        print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')
   
    tasktouserid =TaskToUser.objects.filter(main_task=task_id, kai_user=user)
    today = timezone.localdate()

    notcompletedtasks = TaskToUser.objects.filter(main_task=task_id, status='مسندة')
    countnotcompletedtasks = notcompletedtasks.count()
    status_message=''
    Task_completion_description=''
    attachment=None
    attachment_Task_completion= None
    other_attachments_name =''
    if request.method == 'POST':
        Task_completion_description = request.POST.get('Task_completion_description')
        if 'attachment_Task_completion' in request.FILES:
            attachment_Task_completion = request.FILES['attachment_Task_completion'].read()
            attachment_name = request.FILES['attachment_Task_completion'].name
        else:
            attachment_Task_completion = None
            attachment_name = ''


        attachment_data=[]
        if 'other_attachment_Task_completion' in request.FILES:
            attachments = request.FILES.getlist('other_attachment_Task_completion')

            for attachment_file in attachments:
                attachment_data.append({
                    'content': attachment_file.read(),
                    'name': attachment_file.name,
                })
        if attachment_data:
                for attachmentt in attachment_data:
                    new_file = Files(
                            attachment = attachmentt['content'],
                            attachment_name = attachmentt['name'],
                            taskid = givenTask
                    )
                    new_file.save()

        

        

             
    for task in tasktouserid:
        if task.status != 'مرفوضة':
            task.status = 'منجزة'
            task.addeddate= today
            task.addedtext=Task_completion_description
            task.attachment=attachment_Task_completion
            task.save()
            print(f"Updating task {task.id} with status {task.status}, date {task.addeddate}, description {task.addedtext}")

    if givenTask.full_accomplishment:
        if countnotcompletedtasks-1 > 0 or givenTask.countrejection > 0:
            status_message = f" تم إنجاز جزئياً المهمة من قبل {user.first_name} {user.last_name}"
            givenTask.status = 'منجزة جزئياً'
            givenTask.save()
            status_message_notfy=f" تم إنجاز جزئياً المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
            body = f'''\
            إشعار بإنجاز جزئي للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة {givenTask.task_name}  قد تم إنجازها جزئيًا من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.
        مع خالص التقدير والاحترام,

        بوابة الأعمال

    
           '''

            if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                instructor =givenTask.faculty_initiation
                new_notification = Notification(
                    bu_target=givenTask.faculty_initiation,
                    taskid=givenTask,
                    notification_message=status_message_notfy,
                    function_indicator=2,
                    need_to_be_shown=True)
                new_notification.save()
                bu_collage = givenTask.faculty_initiation.collageid
                if bu_collage and bu_collage.sendNotificationByEmail:
                        send_custom_email(request, bu_collage.buemail, ' إنجاز المهمة جزئياً', body)

            if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:                
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     function_indicator=2, 
                     need_to_be_shown=True)
                new_notification.save()
                if givenTask.kai_initiation.sendNotificationByEmail:
                
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

            نود إعلامكم بأن المهمة {givenTask.task_name}  قد تم إنجازها جزئيًا من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.
        مع خالص التقدير والاحترام,

        بوابة الأعمال

    
           '''
         
            if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                bu_target=givenTask.faculty_initiation,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,
                need_to_be_shown=True)
                new_notification.save()
                bu_collage = givenTask.faculty_initiation.collageid
                if bu_collage and bu_collage.sendNotificationByEmail:
                        send_custom_email(request, bu_collage.buemail, ' إنجاز المهمة جزئياً', body)

            if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:                
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     function_indicator=2, 
                     need_to_be_shown=True)
                new_notification.save()
                if givenTask.kai_initiation.sendNotificationByEmail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', body)
            
            status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
            body = f'''\
            إشعار بإنجاز  للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة {givenTask.task_name}  قد تم إنجازها  من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.
        مع خالص التقدير والاحترام,

        بوابة الأعمال

    
           '''
            
            if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                instructor = givenTask.faculty_initiation
                new_notification = Notification(
                bu_target=givenTask.faculty_initiation,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,
                need_to_be_shown=True)
                new_notification.save()
                bu_collage = givenTask.faculty_initiation.collageid
                if bu_collage and bu_collage.sendNotificationByEmail:
                        send_custom_email(request, bu_collage.buemail, ' إنجاز المهمة ', body)

            if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:                
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     function_indicator=2, 
                     need_to_be_shown=True)
                new_notification.save()
                if givenTask.kai_initiation.sendNotificationByEmail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة ', status_message_notfy)

    else:
        allTaskNotifications = Notification.objects.filter(taskid=givenTask)
        for notification in allTaskNotifications:
            notification.need_to_be_opened=False
            notification.isread = True
            notification.save()


        status_message = f" تم إنجاز المهمة من قبل {user.first_name} {user.last_name}"
        givenTask.status = 'منجزة'
        givenTask.save()
        status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
        body = f'''\
            إشعار بإنجاز  للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة {givenTask.task_name}  قد تم إنجازها  من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.
        مع خالص التقدير والاحترام,

        بوابة الأعمال

    
           '''
         
        if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
                new_notification = Notification(
                bu_target=givenTask.faculty_initiation,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,
                need_to_be_shown=True)
                new_notification.save()
                bu_collage = givenTask.faculty_initiation.collageid
                if bu_collage and bu_collage.sendNotificationByEmail:
                        send_custom_email(request, bu_collage.buemail, ' إنجاز المهمة ', body)
        
        body = f'''\
            إشعار بإنجاز  للمهمة

            السلام عليكم،

            نود إعلامكم بأن المهمة {givenTask.task_name}  قد تم إنجازها  من قبل {user.first_name} {user.last_name} . نشكرهم على ما تم إنجازه حتى الآن ونتطلع إلى استكمال باقي العمل في الوقت المحدد.

            نرجو من الفريق المعني متابعة المهام المتبقية وضمان اكتمالها وفقًا للمعايير المطلوبة.
        مع خالص التقدير والاحترام,

        بوابة الأعمال

    
           '''
        
        if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:                
                new_notification = Notification(
                    kaitarget=givenTask.kai_initiation,
                    taskid=givenTask,
                    notification_message=status_message_notfy,
                    function_indicator=2, 
                    need_to_be_shown=True)
                new_notification.save()
                if givenTask.kai_initiation.sendNotificationByEmail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة ', status_message_notfy)
        
        for id in givenTask.kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)
            new_notification = Notification(
                     kaitarget=instructor ,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     function_indicator=2,
                     need_to_be_shown=True)
            new_notification.save()
            if instructor.sendNotificationByEmail:
                    send_custom_email(request, instructor.email, ' إنجاز المهمة ', body)

        for id in givenTask.faculty_ids :
            instructor =FacultyStaff.objects.get(id=id)
            new_notification = Notification(
                bu_target=instructor,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,
                need_to_be_shown=True)
            new_notification.save()
            bu_collage = instructor.collageid
            if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, ' إنجاز المهمة ', body)

    today = timezone.localdate()
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('head-kai-account:tasks')

@login_required
def MainTask_completion(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    tasktouser =TaskToUser.objects.filter(main_task=task_id, kai_user=user)
    
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
    return redirect('head-kai-account:tasks')

@login_required
@require_POST
def ask_for_pending(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)

    status_message_notfy=f"طلب تعليق المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
    
    body = f'''\
    إشعار طلب تعليق المهمة

    السلام عليكم،

 نود اعلامكم بان هناك طلب تعليق المهمة {givenTask.task_name}   من قبل  {user.first_name} {user.last_name}. نرجو من الجهة المعنية أداء الإجراء المناسب. 

    نشكركم على تعاونكم ونتطلع إلى معالجة هذا الأمر بأسرع وقت ممكن.

    بوابة الأعمال

    
    '''

    if hasattr(givenTask, 'faculty_initiation') and givenTask.faculty_initiation:
            instructor = givenTask.faculty_initiation
            new_notification = Notification(
                bu_target=givenTask.faculty_initiation,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator = 101,     
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
            new_notification.save()
            bu_collage = givenTask.faculty_initiation.collageid
            if bu_collage and bu_collage.sendNotificationByEmail:
                    send_custom_email(request, bu_collage.buemail, 'طلب تعليق المهمة', body)

    if hasattr(givenTask, 'kai_initiation') and givenTask.kai_initiation:                
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                     need_to_be_opened=True,
                     function_indicator = 101,  # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,
                )
                new_notification.save()
                if givenTask.kai_initiation.sendNotificationByEmail:
                    send_custom_email(request, givenTask.kai_initiation.email,'طلب تعليق المهمة', status_message_notfy)
        
    pending_reasons = request.POST.get('pending_reasons')

    # Initialize as lists if they are None
    if givenTask.pending_reasons is None:
        givenTask.pending_reasons = []
    if givenTask.pending_rquestids is None:
        givenTask.pending_rquestids = []

    # Modify the user ID and append to the lists if pending_reasons is provided
    if pending_reasons:
        user_id_modified = 'b.' + str(user.id)
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

    return redirect('head-kai-account:tasks')  # Replace with your actual redirect destination
    
@login_required
def accepte_pending_request(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    notifications = Notification.objects.filter(
                taskid=givenTask,
                kaitarget=user,
                need_to_be_opened=True,
                function_indicator = 101, 
            )
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

    body = f'''\
    إشعار قبول تعليق المهمة

    السلام عليكم،

 نود اعلامكم بانه تم قبول طلب تعليق المهمة {givenTask.task_name}   من قبل  {user.first_name} {user.last_name}. 

    نشكركم على تعاونكم ونتطلع إلى معالجة هذا الأمر بأسرع وقت ممكن.

    بوابة الأعمال

    
    '''
    
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
                          # this is an indicator that will be used when instructor accept or decline a program
                         need_to_be_shown=True,
                    )
                    new_notification.save()
                    if inPending.sendNotificationByEmail:
                        send_custom_email(request, inPending.email,'قبول تعليق المهمة', body)
    
                except Kaibuemployee.DoesNotExist:
            # Handle the case where the Kaibuemployee does not exist
                    print(f"Kaibuemployee with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            elif prefix == 'a':
                try:
            # Query the FacultyStaff table
                    inPending = FacultyStaff.objects.get(pk=user_id)
                    instructor = inPending
                    new_notification = Notification(
                bu_target=instructor,
                taskid=givenTask,
                notification_message=status_message_notfy,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
                    new_notification.save()
                    bu_collage = instructor.collageid
                    if bu_collage and bu_collage.sendNotificationByEmail:
                            send_custom_email(request, bu_collage.buemail, 'قبول تعليق المهمة', body)

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
    givenTask.statusarray.append('تم قبول تعليق المهمة')
    today = timezone.localdate()
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('head-kai-account:tasks')
    
@login_required
def reject_pending_request(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)

    notifications = Notification.objects.filter(
                taskid=givenTask,
                kaitarget=user,
                need_to_be_opened=True,
                function_indicator = 101, 
            )
    
    print("Notifications Found:", notifications.count())

            # Update the retrieved notifications
    for notification in notifications:
                notification.isread = True
                notification.isopened = True
                notification.save()

                notification.refresh_from_db()

    status_message_notfy=f"تم رفض تعليق المهمة {givenTask.task_name}"
    body = f'''\
    إشعار رفض تعليق المهمة

    السلام عليكم،

 نود اعلامكم بانه تم رفض طلب تعليق المهمة {givenTask.task_name}   من قبل  {user.first_name} {user.last_name}. 

    نشكركم على تعاونكم ونتطلع إلى معالجة هذا الأمر بأسرع وقت ممكن.

    بوابة الأعمال

    
    '''
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
                    if inPending.sendNotificationByEmail:
                        send_custom_email(request, inPending.email,'رفض تعليق المهمة', body)
    
                except Kaibuemployee.DoesNotExist:
            # Handle the case where the Kaibuemployee does not exist
                    print(f"Kaibuemployee with id {user_id} does not exist.")
                    continue  # Skip this iteration and continue with the next
            elif prefix == 'a':
                try:
            # Query the FacultyStaff table
                    inPending = FacultyStaff.objects.get(pk=user_id)
                    instructor=inPending
                    new_notification = Notification(
                bu_target=instructor,
                taskid=givenTask,
                notification_message=status_message_notfy,    
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
                    new_notification.save()
                    bu_collage = instructor.collageid
                    if bu_collage and bu_collage.sendNotificationByEmail:
                            send_custom_email(request, bu_collage.buemail, 'رفض تعليق المهمة', body)

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
    givenTask.statusarray.append('تم رفض تعليق المهمة')
    today = timezone.localdate()
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('head-kai-account:tasks')

@login_required
def editTask(request, task_id):
    user = request.user

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )

    notifications_in_programs = Notification.objects.filter(
        kaitarget=user,
        training_program__isnull=False,
        need_to_be_opened=True,
        isopened=False
        )
    
    all_notifications_that_needs_to_be_shown = Notification.objects.filter(kaitarget=user, need_to_be_shown=True)

    all_notifications_that_needs_to_be_shown_count = Notification.objects.filter(
        kaitarget=user, 
        need_to_be_shown=True,
        isread=False
        ).count()
    
    givenTask = get_object_or_404(Task, pk=task_id)

    status_message_notfy=f" تم تعديل تفاصيل البرنامج{givenTask.task_name}"

    context = {
        'task': givenTask,
        'notifications_in_tasks':notifications_in_tasks,
        'notifications_in_programs':notifications_in_programs,
        'all_notifications_that_needs_to_be_shown':all_notifications_that_needs_to_be_shown,
        'all_notifications_that_needs_to_be_shown_count':all_notifications_that_needs_to_be_shown_count, 
        
        # Include other context variables here as needed
    }

    if request.method == 'POST':
        givenTask.task_description = request.POST['taskdescription'] 
        givenTask.end_date = request.POST['enddate']
        givenTask.save()
        status_message = f" تم تعديل تفاصيل المهمة من قبل {user.first_name} {user.last_name} "
        givenTask.statusarray.append(status_message)
        today = timezone.localdate()
        givenTask.datearray.append(today)
        attachment_data = []
        if 'attachment' in request.FILES:
            attachments = request.FILES.getlist('attachment')

            for attachment_file in attachments:
                attachment_data.append({
                    'content': attachment_file.read(),
                    'name': attachment_file.name,
                })
        if attachment_data:
                for attachmentt in attachment_data:
                    new_file = Files(
                            attachment = attachmentt['content'],
                            attachment_name = attachmentt['name'],
                            taskid = givenTask
                    )
                    new_file.save()
        return redirect('head-kai-account:task-detail', task_id=task_id)

    # Correct usage of render
    return render(request, 'kai/Task_edit.html', context)

@login_required
def send_to_new_Instructor(request, task_id ):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    givenTask.countrejection = 0
    givenTask.save()

    body = f'''\
        السلام عليكم،

        نود إعلامكم بأن مهمة جديدة بعنوان {givenTask.task_name}  قد تم تكليفها إليكم. نأمل منكم البدء في تنفيذ المهمة وفقاً للمتطلبات المحددة.  

        نشكركم مقدماً على جهودكم ونتطلع إلى إنجازكم لهذا العمل بالجودة والكفاءة المعهودة.

        مع خالص التقدير والاحترام,

        بوابة الأعمال
        '''

    notifications = Notification.objects.filter(
                taskid=givenTask,
                kaitarget=user,
                need_to_be_opened=True,
                function_indicator = 202, 
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
            
            assiningto = request.POST.getlist('assiningto2')
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
                instructor=faculty
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
                bu_target=instructor,
                taskid=givenTask,
                notification_message=status_message_notfy,
                function_indicator=2,    
                need_to_be_opened=True,
                # this is an indicator that will be used when instructor accept or decline a program
                need_to_be_shown=True,
                )
                new_notification.save()
                bu_collage = instructor.collageid
                if bu_collage and bu_collage.sendNotificationByEmail:
                        send_custom_email(request, bu_collage.buemail, 'مهمة مسندة', body)

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
                print('facultyTaskToUser')

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
                if kaiuser.sendNotificationByEmail:
                    send_custom_email(request, kaiuser.email, 'مهمة مسندة', status_message)

            if givenTask.status =='منجزة جزئياً، مرفوضة من البعض':
                givenTask.status =  'منجزة جزئياً'
            else:
                givenTask.status = tempStatus2
        
            givenTask.statusarray.append(tempStatus)
            today = timezone.localdate()
            givenTask.datearray.append(today)
            givenTask.save()
    return redirect('head-kai-account:tasks')


##################### Email #####################

def send_custom_email(request, receiver_email, topic, message):   
    subject = topic
    body = message
    # Create MIMEText object with the body text and charset
    body_mime = MIMEText(body, 'plain', 'utf-8')
    receiver_email = '442200922@student.ksu.edu.sa' 
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
    all_notifications_that_needs_to_be_shown = Notification.objects.filter(kaitarget=user, need_to_be_shown=True)
    for totify in all_notifications_that_needs_to_be_shown:
        totify.isread = True
        totify.save()
    return HttpResponse(status=204)

@login_required
def update_notifications_ajax_Delete(request, notification_id):
    user = request.user
    givenNotification = get_object_or_404(Notification, id=notification_id)
    givenNotification.need_to_be_shown=False
    givenNotification.save()
    return HttpResponse(status=204)

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
    return redirect('head-kai-account:kai-home')
