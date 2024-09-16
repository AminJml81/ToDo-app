from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "POST"):
            return TaskCreateUpdateSerializer
        return TaskReadSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['version'] = 'api-v5'
        return context