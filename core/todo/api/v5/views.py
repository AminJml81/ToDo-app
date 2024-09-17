from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ...models import Task
from ..serializers import(
                           TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer
                        )
from ..filterset import TaskFilter


class TaskViewSet(ModelViewSet):
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskUpdateSerializer
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskReadSerializer
    