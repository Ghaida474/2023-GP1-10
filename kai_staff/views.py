from datetime import timezone
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from app.forms import updateKai,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages
from app.models import FacultyStaff,Collage, Trainingprogram,Register,Trainees,StatusDateCheck, Notification , Kaibuemployee , Task , TaskToUser
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

################### coomunication  ###################
@login_required
def chat(request):
    username = request.user.username
    secret = request.user.id
    users = filteredUsers(request)
    return render(request, 'kai_staff/chat.html' , {'username':username , 'secret': secret ,'users':users})

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
    return render(request, 'kai_staff/chat.html' , context)

@login_required
def callsDashboard(request):
    return render(request, 'kai_staff/calls-dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    return render(request, 'kai_staff/videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required
def joinroom(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/kai_staff/kaistaff-home/videocall?roomID=" + roomID)
    return render(request, 'kai_staff/joinroom.html')

################### Profile  ###################
@login_required
def kaistaff_home (request):
    user = request.user
    if user.new_user:
        return redirect('kai_staff:change_new_user_password')
    return render(request, 'kai_staff/Home.html', {'user': user })

@login_required
def change_new_user_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.new_user = False
        user.save()
        return redirect('kai_staff:kaistaff-home')
    return render(request, 'kai_staff/new-use-reset-password.html')
   
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
    success = False
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            success = True
            # return redirect('kai_staff:profile')

    return render(request, 'kai_staff/change-password.html', {'user': user, 'form': form , 'success':success})

################### Training program  ###################
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


################Tasks ###################

from django.db.models import Case, When, Value, IntegerField, DateTimeField, CharField
@login_required
def task_view(request):
    user = request.user
    current_date = timezone.now()

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
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
    Dean = Kaibuemployee.objects.filter(position='رئيس المعهد')
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
           attachment = attachment,
           toall=ToAll,
           full_accomplishment = full_accomplishment1 
        )
        new_task.save()
         
        
        status_message_notfy = f"تم اسناد مهمة {new_task.task_name} إليك الرجاء إنجاز المهمة"

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
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', status_message)
        
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
            print("in the loop")
            print(new_notification.need_to_be_shown)
          
            if instructor.sendnotificationbyemail:
                send_custom_email(request, instructor.email, 'مهمة مسندة', status_message)









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
        return redirect('kai_staff:tasks')
    current_date =timezone.now().date()

    
    

       
    
            
        



    return render(request, 'kai_staff/Tasks.html', {'user': user, 'allCollages':allCollages, 'allTasksAssignedByUser':allTasksAssignedByUser, 'allTasksAssignedToUser':allTasksAssignedToUser, 'all_tasks_related_to_user':all_tasks_related_to_user, 'allFaculties':allFaculties, 'allKaiEmployees':allKaiEmployees, 'otherCollagesBUHeads':otherCollagesBUHeads, 'Dean':Dean, 'notifications_in_tasks':notifications_in_tasks,
                                                     'notifications_in_assigned_by_user_tasks_count': notifications_in_assigned_by_user_tasks_count,
                                                     'notifications_in_assigned_to_user_tasks_count':notifications_in_assigned_to_user_tasks_count,
                                                     'notifications_in_related_ended_user_tasks_count':notifications_in_related_ended_user_tasks_count,
                                                     'notifications_in_assigned_by_user_tasks':notifications_in_assigned_by_user_tasks,
                                                     'notifications_in_assigned_to_user_tasks':notifications_in_assigned_to_user_tasks,
                                                     'notifications_in_related_ended_user_tasks':notifications_in_related_ended_user_tasks,
                                                     'combined_tasks_ids':combined_tasks_ids,
                                                     'current_date':current_date,

                                                     })

from django.db.models import Q, Case, When, IntegerField

@login_required
def task_details(request, task_id):
    user = request.user

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    
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
           attachment = attachment,
           main_task=main_task_instance,
           toall=ToAll,
           full_accomplishment = full_accomplishment1 

        )
        new_task.save()



        status_message_notfy = f"تم اسناد مهمة {new_task.task_name} إليك الرجاء إنجاز المهمة"

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
                send_custom_email(request, instructor.email, 'مهمة مسندة', status_message_notfy)
        
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
                send_custom_email(request, instructor.email, 'مهمة مسندة', status_message_notfy)





    

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
        return redirect('kai_staff:task-detail', task_id=task_id)
    
    pending_reasons = givenTask.pending_reasons if givenTask.pending_reasons is not None else []
    status_with_dates = zip(givenTask.datearray, givenTask.statusarray)
    zipped_names_reasons = zip(pending_requestor_names, pending_reasons)
    current_date = timezone.now().date()








    return render(request, 'kai_staff/Task_view.html',{'givenTask':givenTask, 'allCollages':allCollages, 'otherCollagesBUHeads':otherCollagesBUHeads,'all_tasks_related_to_user':all_tasks_related_to_user, 'allTasksAssignedToUser':allTasksAssignedToUser, 'subTasksCount':subTasksCount,'NotCompletedSubTasks':NotCompletedSubTasks, 'Faculty_user':Faculty_user, 'Kai_user':Kai_user, 'userAssignment':userAssignment,'userAccompleshment':userAccompleshment, 'userrejection':userrejection, 'pending_requestor_names':pending_requestor_names, 'zipped_names_reasons':zipped_names_reasons, 'status_with_dates':status_with_dates, 'flat_hierarchy':flat_hierarchy, 'not_completed_subtasks_count':not_completed_subtasks_count, 'recent_rejected_tasks':recent_rejected_tasks, 'notifications_in_tasks':notifications_in_tasks, 'current_date':current_date})


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

    print("Notifications Found:", notifications.count())

    status_message_notfy=f"تم استرجاع المهمة {givenTask.task_name}"

   


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
                send_custom_email(request, instructor.email, 'إسترجاع المهمة', status_message_notfy)
        
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
                send_custom_email(request, instructor.email, 'مهمة مسندة', status_message_notfy)




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
    


    return redirect('kai_staff:tasks')

@login_required
def reject_task(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)

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
    if givenTask.faculty_initiation:
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
                send_custom_email(request, givenTask.faculty_initiation .email, 'رفض المهمة', status_message_notfy)
        
        
    if givenTask.kai_initiation:
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
                send_custom_email(request, givenTask.kai_initiation.email, 'رفض المهمة', status_message_notfy)
        



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

    return redirect('kai_staff:tasks')
    
@login_required
def Task_completion(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)


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

                print(f'Notification ID: {notification.id}, isopened: {notification.isopened}, isread: {notification.isread}')


   
    tasktouserid =TaskToUser.objects.filter(main_task=task_id, kai_user=user)
    today = timezone.localdate()

    notcompletedtasks = TaskToUser.objects.filter(main_task=task_id, status='مسندة')
    countnotcompletedtasks = notcompletedtasks.count()
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
    for task in tasktouserid:
        if task.status != 'مرفوضة':
            task.status = 'منجزة'
            task.addeddate= today
            task.addedtext=taskdescription
            task.attachment=attachment
            task.save()
    

    
    
    if givenTask.full_accomplishment:
        if countnotcompletedtasks-1 > 0 or givenTask.countrejection > 0:
            status_message = f" تم إنجاز جزئياً المهمة من قبل {user.first_name} {user.last_name}"
            givenTask.status = 'منجزة جزئياً'
            givenTask.save()


            status_message_notfy=f" تم إنجاز جزئياً المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
         

            if givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة جزئياً', status_message_notfy)
        
        
            if givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', status_message_notfy)
        


            if givenTask.countrejection: 
                givenTask.status = 'منجزة جزئياً، مرفوضة من البعض'
                givenTask.save()

        else:
            status_message = f" تم إنجاز المهمة من قبل {user.first_name} {user.last_name}"
            givenTask.status = 'منجزة'
            givenTask.save()

            status_message_notfy=f" تم إنجاز جزئياً المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
         

            if givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة جزئياً', status_message_notfy)
        
        
            if givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', status_message_notfy)
            
            status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
         

            if givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة ', status_message_notfy)
        
        
            if givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة جزئياً', status_message_notfy)
        
        


    else:
        status_message = f" تم إنجاز المهمة من قبل {user.first_name} {user.last_name}"
        givenTask.status = 'منجزة'
        givenTask.save()

        status_message_notfy=f" تم إنجاز  المهمة {givenTask.task_name}"
         

        if givenTask.faculty_initiation:
                new_notification = Notification(
                  faculty_target=givenTask.faculty_initiation ,
                  taskid=givenTask,
                   notification_message=status_message_notfy,
                         
                   
                   function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                   need_to_be_shown=True,

                 )
                new_notification.save()
                if givenTask.faculty_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.faculty_initiation .email, ' إنجاز المهمة ', status_message_notfy)
        
        
        if givenTask.kai_initiation:
                new_notification = Notification(
                     kaitarget=givenTask.kai_initiation,
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
                new_notification.save()
                if givenTask.kai_initiation.sendnotificationbyemail:
                    send_custom_email(request, givenTask.kai_initiation.email, ' إنجاز المهمة ', status_message_notfy)
        for id in givenTask.kai_ids:
            instructor = Kaibuemployee.objects.get(id=id)
            new_notification = Notification(
                     kaitarget=instructor ,
                  
                     taskid=givenTask,
                     notification_message=status_message_notfy,
                         
            
                     function_indicator=2, # this is an indicator that will be used when instructor accept or decline a program
                     need_to_be_shown=True,

                )
            new_notification.save()
            if instructor.sendnotificationbyemail:
                    send_custom_email(request, instructor.email, ' إنجاز المهمة ', status_message_notfy)

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
                    send_custom_email(request, instructor.email, ' إنجاز المهمة ', status_message_notfy)

        
    
    today = timezone.localdate()
    givenTask.statusarray.append(status_message)
    givenTask.datearray.append(today)
    givenTask.save()


    return redirect('kai_staff:tasks')

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
    return redirect('kai_staff:tasks')


@login_required
@require_POST
def ask_for_pending(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)


    status_message_notfy=f"طلب تعليق المهمة {givenTask.task_name} من قبل {user.first_name} {user.last_name}"
         

    if givenTask.faculty_initiation:
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
        
        
    if givenTask.kai_initiation:
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

    return redirect('kai_staff:tasks')  # Replace with your actual redirect destination
    
@login_required
def accepte_pending_request(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
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
    givenTask.statusarray.append('تم قبول تعليق المهمة')
    today = timezone.localdate()
    givenTask.datearray.append(today)
    givenTask.save()
    return redirect('kai_staff:tasks')
    
@login_required
def reject_pending_request(request, task_id):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)

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
                    if inPending.sendnotificationbyemail:
                        send_custom_email(request, inPending.email,'رفض تعليق المهمة', status_message_notfy)
    

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
                        send_custom_email(request, inPending.email,'رفض تعليق المهمة', status_message_notfy)
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
    return redirect('kai_staff:tasks')


@login_required
def editTask(request, task_id):
    user = request.user

    notifications_in_tasks = Notification.objects.filter(
        kaitarget=user,
        taskid__isnull=False,
        need_to_be_opened=True,
        isopened=False
    )
    
    givenTask = get_object_or_404(Task, pk=task_id)

    status_message_notfy=f" تم تعديل تفاصيل البرنامج{givenTask.task_name}"

   


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
                send_custom_email(request, instructor.email, 'تعديل تفاصيل البرنامج', status_message_notfy)
        
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
                send_custom_email(request, instructor.email, 'تعديل تفاصيل البرنامج', status_message_notfy)


    context = {
        'task': givenTask,
        'notifications_in_tasks':notifications_in_tasks,
        
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
    return render(request, 'kai_staff/Task_edit.html', context)


@login_required
def send_to_new_Instructor(request, task_id ):
    user = request.user
    givenTask = get_object_or_404(Task, pk=task_id)
    givenTask.countrejection = 0
    givenTask.save()

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
    return redirect('kai_staff:tasks')

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

###########app heder notification######################
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
    # Retrieve the logged-in user
    user = request.user

    givenNotification = get_object_or_404(Notification, id=notification_id)
    givenNotification.need_to_be_shown=False
    givenNotification.save()

    
    return HttpResponse(status=204)