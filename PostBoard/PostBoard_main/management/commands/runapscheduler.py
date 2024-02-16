import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from PostBoard_main.models import Posts
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Posts.objects.filter(time_in__gte=last_week)
    text = '\n'.join(['{} - {} - {}'.format(p.headline, p.category, f'http://127.0.0.1:8000{p.get_absolute_url()}') for p in posts])
    subject = f'Еженедельная рассылка по подпискам'
    cat_id = [p.category_id for p in posts]
    emails = User.objects.filter(
        subscriptions__to_category=cat_id[0]
    ).values_list('email', flat=True)
    for email in emails:
        msg = EmailMultiAlternatives(subject, text, None, [email])
        msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                # day_of_week="mon", hour="00", minute="00"
                second="*/10"
            ),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Запускаю расписание...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Расписание останавливается...")
            scheduler.shutdown()
            logger.info("Расписание остановленно!")
