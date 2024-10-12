from django.urls import path, include

from todo.views import (
    ListTasksView,
    TaskUpdateView,
    CreateTaskView,
    DeleteTaskView,
    TaskDetailView,
)


app_name = "todo"

urlpatterns = [
    path("create/", CreateTaskView.as_view(), name="task-create"),
    path("", ListTasksView.as_view(), name="task-list"),
    path("<slug:slug>/", TaskDetailView.as_view(), name="task-detail"),
    path("<slug:slug>/delete/", DeleteTaskView.as_view(), name="task-delete"),
    path("<slug:slug>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("api/v1/", include("todo.api.v1.urls")),
    path("api/v2/", include("todo.api.v2.urls")),
    path("api/v3/", include("todo.api.v3.urls")),
    path("api/v4/", include("todo.api.v4.urls")),
    path("api/v5/", include("todo.api.v5.urls")),
]
