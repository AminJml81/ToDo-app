import os

from celery import Celery

# from todo.tasks import *

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()


app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# NOTE: METHOD 2 to add celery beat(periodic task).
# -------------------------------------------------
# from celery.schedules import crontab
# from todo.tasks import delete_user_tasks, delete_unverifed_users


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute=10),
#         delete_user_tasks.s(),
#         name="delete user tasks every 10 minutes.",
#     )
#     sender.add_periodic_task(
#         crontab(hour=0),
#         delete_unverifed_users.s(),
#         name="delete unverified users every 24 hours.",
#     )
