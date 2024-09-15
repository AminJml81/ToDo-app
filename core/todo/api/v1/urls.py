from django.urls import path

from .views import tasks_list_create, task_retrive_update_delete

app_name = 'api-v1'

urlpatterns = [
    path('', tasks_list_create, name='list-tasks'),
    path('create/', tasks_list_create, name='task-create'),
    path('<int:task_id>/', task_retrive_update_delete, name='task-retrieve-update-delete')

]
