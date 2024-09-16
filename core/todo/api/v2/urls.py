from django.urls import path

from .views import ListCreateTaskAPIView, RetriveUpdateDeleteTaskAPIView

app_name = 'api-v2'

urlpatterns = [
    path('', ListCreateTaskAPIView.as_view(), name='task-list-create'),
    path('<int:task_id>/', RetriveUpdateDeleteTaskAPIView.as_view(), name='task-detail' )
]
