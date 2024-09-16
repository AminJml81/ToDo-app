from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer
from ..filterset import TaskFilter

class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "POST"):
            return TaskCreateUpdateSerializer
        return TaskReadSerializer
    