from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django.core.cache import cache

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer

from ..filterset import TaskFilter


class ListCreateTaskGenericView(ListCreateAPIView):
    filterset_class = TaskFilter
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskReadSerializer

    def get_queryset(self):
        user = self.request.user
        tasks = cache.get_or_set(
            f"{user}--tasks", Task.objects.filter(user=user), timeout=5 * 60
        )
        return tasks

    def post(self, request, *args, **kwargs):
        reponse = super().post(request, *args, **kwargs)
        if reponse.status_code == 201:
            cache.delete(f"{self.request.user}--tasks")
        return reponse


class RetriveUpdateDeleteTaskGenericView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskUpdateSerializer
        return TaskReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete(f"{self.request.user}--tasks")
        return response

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete(f"{self.request.user}--tasks")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete(f"{self.request.user}--tasks")
        return response
