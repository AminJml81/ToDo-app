from rest_framework.viewsets import ModelViewSet

from django.core.cache import cache

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer
from ..filterset import TaskFilter


class TaskViewSet(ModelViewSet):
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        tasks = cache.get_or_set(
            f"{user}--tasks", Task.objects.filter(user=user), timeout=5 * 60
        )
        return tasks

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskUpdateSerializer
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskReadSerializer

    def update(self, request, *args, **kwargs):
        reponse = super().update(request, *args, **kwargs)
        if reponse.status_code == 200:
            cache.delete(f"{self.request.user}--tasks")
        return reponse

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete(f"{self.request.user}--tasks")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete(f"{self.request.user}--tasks")
        return response
