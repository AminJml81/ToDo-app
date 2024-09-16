from django.urls import path

from .views import ListCreateTaskGenericView, RetriveUpdateDeleteTaskGenericView

app_name = 'api-v3'

urlpatterns = [
    path('', ListCreateTaskGenericView.as_view(), name='task-list-create'),
    path('<int:pk>/', RetriveUpdateDeleteTaskGenericView.as_view(), name='task-detail' )
]
