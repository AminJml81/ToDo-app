from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ...models import Task
from ..serializers import(
                        TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer
                        )
from ..pagination import CustomPagination
from ..filterset import TaskFilter


class ListCreateTaskGenericView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)            

    def get(self, request, *args, **kwargs):
        paginator = CustomPagination()
        tasks = self.get_queryset()
        filtered_tasks = self.filter_queryset(tasks)
        tasks_page = paginator.paginate_queryset(filtered_tasks, request)
        serializer = self.get_serializer(tasks_page, many=True,
                                        context={'request':self.request})
        return Response(serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        receive_data = request.data
        serializer = self.get_serializer(data=receive_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetriveUpdateDeleteTaskGenericView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return TaskUpdateSerializer
        return TaskReadSerializer
        
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
    
    def get(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)         

    def put(self, request, *args, **kwargs):
        return self.update(request, False)   

    def patch(self, request, *args, **kwargs):
        return self.update(request, True) 

    def update(self, request, partial):
        # main task of updating based on partial parameter
        # True for PATCH, False for PUT
        task = self.get_object()
        update_data = request.data
        serializer = self.get_serializer(instance=task, data=update_data,
                                        partial=partial)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)