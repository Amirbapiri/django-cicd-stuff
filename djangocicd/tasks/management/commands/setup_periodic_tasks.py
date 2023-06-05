from django.core.management import BaseCommand
from django.utils.timezone import get_default_timezone_name
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from djangocicd.users.tasks import profile_information_update as profile_update_task


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **kwargs):
        print("deleting all periodic tasks and schedules".upper())


        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()
        
        """
        {
            'task': 'periodic_task_description' ,
            'name': 'description',
            'cron': {
                'minute': '*',
                'hour': '*',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'enabled': True,
        }
        """

        periodic_tasks_data = [
            {
                'task': profile_update_task,
                'name': "Update user's profile information task",
                'cron': {
                    'minute': '45',
                    'hour': '3',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True,
            },
        ]
        timezone = get_default_timezone_name()

        for periodic_task in periodic_tasks_data:
            print(f"Setting up {periodic_task['task'].name}")

            cron = CrontabSchedule.objects.create(
                timezone=timezone,
                **periodic_task["cron"],
            )

            PeriodicTask.objects.create(
                name=periodic_task["name"],
                task=periodic_task["task"].name,
                crontab=cron,
                enabled=periodic_task["enabled"],
            )

