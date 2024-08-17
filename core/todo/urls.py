from django.urls import path

from todo.views import (
    ListTasksView, TaskUpdateView, CreateTaskView, DeleteTaskView, TaskDetailView)


app_name = 'todo'

urlpatterns = [
    path('create/', CreateTaskView.as_view(), name='task-create'),
    path('', ListTasksView.as_view(), name='task-list'),
    path('<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('<slug:slug>/delete/', DeleteTaskView.as_view(), name='task-delete'),
    path('<slug:slug>/update/', TaskUpdateView.as_view(), name='task-update'),

]
