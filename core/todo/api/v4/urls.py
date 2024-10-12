from django.urls import path

from .views import ListCreateTaskGenericView, RetriveUpdateDeleteTaskGenericView

app_name = "api-v4"

urlpatterns = [
    path("", ListCreateTaskGenericView.as_view(), name="task-list-create"),
    path(
        "<slug:slug>/", RetriveUpdateDeleteTaskGenericView.as_view(), name="task-detail"
    ),
]
