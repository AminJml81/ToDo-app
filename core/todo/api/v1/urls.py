from django.urls import path

from .views import list_create_task, retrive_update_delete_task

app_name = "api-v1"

urlpatterns = [
    path("", list_create_task, name="task-list-create"),
    path("<slug:slug>/", retrive_update_delete_task, name="task-detail"),
]
