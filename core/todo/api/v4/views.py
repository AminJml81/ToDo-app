from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer


class ListCreateTaskGenericView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateUpdateSerializer
        return TaskReadSerializer
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
        

class RetriveUpdateDeleteTaskGenericView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskCreateUpdateSerializer
        return TaskReadSerializer
        
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)