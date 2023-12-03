import logging
from django.utils import timezone
from app.models import Trainingprogram, StatusDateCheck
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