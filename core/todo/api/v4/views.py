from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

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
        return Task.objects.filter(user=user)


class RetriveUpdateDeleteTaskGenericView(RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskUpdateSerializer
        return TaskReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
