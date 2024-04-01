import logging
from django.utils import timezone
from app.models import Trainingprogram, StatusDateCheck, FacultyStaff, Notification, Task, TaskToUser, Kaibuemployee
from .utils import send_custom_email
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def update_program_status():

    logger.info("Task started")

    # Get only released programs
    programs = Trainingprogram.objects.filter(isreleased_field=True)
    now = timezone.now().date()

    for program in programs:
        status_check = StatusDateCheck.objects.filter(training_program=program)
        yesterday = now - timezone.timedelta(days=1)
        tomorrow = now + timezone.timedelta(days=1)

        if program.lastenrollmentdate == yesterday:
            program.status="انتهى تسجيل المتدربين"
            status_check.filter(status="انتهى تسجيل المتدربين").update(indicator='T')
            status_check.filter(status="انتهى تسجيل المتدربين").update(date=timezone.now().date())
        
        elif program.startdate == now:
            program.status="بدأ البرنامج"
            status_check.filter(status="بدأ البرنامج").update(indicator='T')
            status_check.filter(status="بدأ البرنامج").update(date=timezone.now().date())

        elif program.enddate == yesterday:
            program.status="إنتهاء البرنامج"
            status_check.filter(status="إنتهاء البرنامج").update(indicator='T')
            status_check.filter(status="إنتهاء البرنامج").update(date=timezone.now().date())

        program.save()

    logger.info("Task done")
    return 'Task completed successfully'


@shared_task
def notify_task_due_dates():
    logger.info("Notification Task started")

    # Retrieve all tasks that are not completed or retracted
    tasks = Task.objects.exclude(status__in=['منجزة', 'مسترجعة'])

    for task in tasks:
        task_results = TaskToUser.objects.filter(main_task=task, status='مسندة')
        faculty_ids = []
        kai_ids = []

        # Retrieve faculty and kai user ids
        for task_result in task_results:
            if task_result.faculty_user is not None:
                faculty_ids.append(task_result.faculty_user.id)
            if task_result.kai_user is not None:
                kai_ids.append(task_result.kai_user.id)

        # Determine when to send notifications
        today = timezone.now().date()
        days_until_due = (task.end_date - today).days

        # Set status_message_notfy based on the time until the task is due
        status_message_notfy = None
        if task.priority == 'عاجلة':
            if days_until_due == 4 or days_until_due == 2 or days_until_due == 0:
                if days_until_due == 4:
                    status_message_notfy = f"تبقى ٤ ايام على اخر يوم لإنجاز المهمة المسندة إليك {task.task_name} الرجاء إنجاز المهمة"
                elif days_until_due == 2:
                    status_message_notfy = f"تبقى يومان ايام على اخر يوم لإنجاز المهمة المسندة إليك {task.task_name} الرجاء إنجاز المهمة"
                elif days_until_due == 0:
                    status_message_notfy = f"اليوم أخر يوم لتسليم المهمة المسندة اليك بعد ذلك ستصبح المهمة متاخرة {task.task_name} الرجاء إنجاز المهمة"
        else:
            if days_until_due == 2 or days_until_due == 0 or days_until_due == -1:
                if days_until_due == 2:
                    status_message_notfy = f"تبقى يومان ايام على اخر يوم لإنجاز المهمة المسندة إليك {task.task_name} الرجاء إنجاز المهمة"
                elif days_until_due == 0:
                    status_message_notfy = f"اليوم أخر يوم لتسليم المهمة المسندة اليك بعد ذلك ستصبح المهمة متاخرة {task.task_name} الرجاء إنجاز المهمة"
                elif days_until_due == -1:
                    status_message_notfy = f"أصبحت المهمة متأخرة {task.task_name} الرجاء إنجاز المهمة المتأخرة"

        # Only proceed if there's a notification message to send
        if status_message_notfy:
            # Notify Kaibu employees
            for id in kai_ids:
                instructor = Kaibuemployee.objects.get(id=id)
                new_notification = Notification(
                    kaitarget=instructor,
                    taskid=task,
                    notification_message=status_message_notfy,
                    function_indicator=2,  # This is an indicator used when instructor accepts or declines a program
                    need_to_be_shown=True,
                )
                new_notification.save()

                if instructor.sendnotificationbyemail:
                    send_custom_email(None, instructor.email, 'تذكير بإنجاز المهمة', status_message_notfy)

            # Notify faculty staff
            for id in faculty_ids:
                instructor = FacultyStaff.objects.get(id=id)
                new_notification = Notification(
                    faculty_target=instructor,
                    taskid=task,
                    notification_message=status_message_notfy,
                    function_indicator=2,  # This is an indicator used when instructor accepts or declines a program
                    need_to_be_shown=True,
                )
                new_notification.save()

                if instructor.sendnotificationbyemail:
                    send_custom_email(None, instructor.email, 'تذكير بإنجاز المهمة', status_message_notfy)

    logger.info("Notification Task done")
    return 'Notification task completed successfully'

from celery import shared_task
from app.models import Project, FacultyStaff, Notification
from django.core.mail import send_mail
import datetime

@shared_task
def send_project_reminders():

    allProjects = Project.objects.all()

    for prj in allProjects:

        buHead = FacultyStaff.objects.filter(collageid=prj.collageid, is_buhead=True)

        teamMember = FacultyStaff.objects.filter(id__in=prj.teamid)

        if prj.enddate and prj.enddate <= datetime.date.today() + datetime.timedelta(days=2):

            for id in teamMember:

                status_message_notfy = f"أخر يوم لتسليم المشروع {prj.Name} بعد يومين الرجاء تسليم المشروع عاجلا"

                new_notification = Notification(

                    faculty_target = id,
                    notification_message =status_message_notfy,
                    need_to_be_shown = True,
                )

                new_notification.save()
                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, 'تذكير بتسليم المشروع', status_message_notfy)


            for head in buHead:

                status_message_notfy = f"أخر يوم لتسليم المشروع {prj.Name} بعد يومين الرجاء تسليم المشروع عاجلا"

                new_notification = Notification(
                    faculty_target=head,
                    notification_message=status_message_notfy,
                    need_to_be_shown=True
                )
                new_notification.save()

                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, 'تذكير بتسليم المشروع', status_message_notfy)


        if prj.enddate and prj.enddate == datetime.date.today() + datetime.timedelta(days=1):

            status_message_notfy= f"أخر يوم لتسليم المشروع  {prj.Name}غداً  الرجاء تسليم المشروع عاجلا "
            for id in teamMember:
                new_notification = Notification(

                faculty_target = id,
                 notification_message =status_message_notfy,
                 need_to_be_shown = True,
                )

                new_notification.save()
                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, 'تذكير بتسليم المشروع', status_message_notfy)

  
            for head in buHead:

                status_message_notfy= f"أخر يوم لتسليم المشروع  {prj.Name}غداً  الرجاء تسليم المشروع عاجلا "

                new_notification = Notification(
                    faculty_target=head,
                    notification_message=status_message_notfy,
                    need_to_be_shown=True
                )
                new_notification.save()

                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, 'تذكير بتسليم المشروع', status_message_notfy)

                        

        if prj.questiondeadline and prj.questiondeadline == datetime.date.today() + datetime.timedelta(days=1):

            for id in teamMember:

                status_message_notfy= f"غداً اخر يوم لإستقبال الأسئلة بخصوص  {prj.Name} "


                new_notification = Notification(

                faculty_target = id,
                 notification_message =status_message_notfy,
                 need_to_be_shown = True,




                )
                new_notification.save()
                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' تذكير بموعد استقبال الأسئلة   ', status_message_notfy)

            


            for head in buHead:

                status_message_notfy= f"غداً اخر يوم لإستقبال الأسئلة بخصوص  {prj.Name} "

                new_notification = Notification(
                    faculty_target=head,
                    notification_message=status_message_notfy,
                    need_to_be_shown=True
                )
                new_notification.save()

                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' تذكير بموعد استقبال الأسئلة   ', status_message_notfy)


            # Same logic to send question deadline 1 day reminder
            

        if prj.proposaldeadline and prj.proposaldeadline <= datetime.date.today() + datetime.timedelta(days=2):
            for id in teamMember:

                status_message_notfy= f" اخر يوم لإسقبال العرض لمشروع   {prj.Name}  خلال يومان "


                new_notification = Notification(

                faculty_target = id,
                 notification_message =status_message_notfy,
                 need_to_be_shown = True,




                )
                new_notification.save()
                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' اخر يوم لإسقبال العرض لمشروع  ', status_message_notfy)

            


            for head in buHead:

                status_message_notfy= f" اخر يوم لإسقبال العرض لمشروع   {prj.Name}  خلال يومان "

                new_notification = Notification(
                    faculty_target=head,
                    notification_message=status_message_notfy,
                    need_to_be_shown=True
                )
                new_notification.save()

                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' اخر يوم لإسقبال العرض لمشروع  ', status_message_notfy)


            # Same logic to send proposal deadline 2 day reminder

        if prj.proposaldeadline and prj.proposaldeadline == datetime.date.today() + datetime.timedelta(days=1):

            status_message_notfy= f"اخر يوم لإسقبال العرض لمشروع   {prj.Name}  غداً "

            for id in teamMember:
                new_notification = Notification(

                faculty_target = id,
                 notification_message =status_message_notfy,
                 need_to_be_shown = True,




                )
                new_notification.save()
                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' اخر يوم لإسقبال العرض لمشروع  ', status_message_notfy)

            


            for head in buHead:

                status_message_notfy= f"اخر يوم لإسقبال العرض لمشروع   {prj.Name}  غداً "

                new_notification = Notification(
                    faculty_target=head,
                    notification_message=status_message_notfy,
                    need_to_be_shown=True
                )
                new_notification.save()

                if id.sendnotificationbyemail:
                    send_custom_email(None, id.email, ' اخر يوم لإسقبال العرض لمشروع  ', status_message_notfy)
    logger.info("Notification Project done")
    return 'Notification task Project successfully'


            # Same logic to send proposal deadline 1 day reminder