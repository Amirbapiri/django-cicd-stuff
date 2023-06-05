from celery import shared_task

from djangocicd.users.services import profile_information_update_task


@shared_task
def profile_information_update():
    profile_information_update_task()

