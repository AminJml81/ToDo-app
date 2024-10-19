from django.contrib.auth import get_user_model

from todo.models import Task

from celery import shared_task


@shared_task
def delete_user_tasks():
    # Delete tasks of verified and not superuser each 10 minutes.
    users = get_user_model().objects.filter(is_verified=True)
    users = users.exclude(is_superuser=True)
    for user in users:
        tasks = Task.objects.filter(user=user)
        tasks.delete()


@shared_task
def delete_unverifed_users():
    # Delete unverified users every 24 hours.
    unverified_users = get_user_model().objects.filter(is_verified=False)
    unverified_users = unverified_users.exclude(is_superuser=True)
    unverified_users.delete()
