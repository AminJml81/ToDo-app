from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..pagination import CustomPagination
from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer
from ..filterset import TaskFilter


class ListCreateTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # task lists
        paginator = CustomPagination()
        tasks = Task.objects.filter(user=request.user)
        filtered_tasks = self.filter_tasks(request, tasks)
        filtered_tasks = self.search_tasks(request, filtered_tasks)
        tasks_page = paginator.paginate_queryset(filtered_tasks, request)
        serializer = TaskReadSerializer(tasks_page, many=True, context={'request':request})
        return Response(serializer.data)
    

    def filter_tasks(self, request, tasks):
        # getting status, title, description query parameter and 
        # filter the tasks
        status = request.query_params.get('status')
        title = request.query_params.get('title')
        description = request.query_params.get('description')
        if status:
            tasks = tasks.filter(status=status)
        if title:
            tasks = tasks.filter(title__icontains=title)
        if description:
            tasks = tasks.filter(description__icontains=description)
        return tasks
    
    def search_tasks(self, request, tasks):
        search_key = request.query_params.get('search')
        tasks = tasks.filter(Q(title__icontains=search_key) |
                            Q(description__icontains=search_key))
        return tasks
    
    def post(self, request):
        # create new task
        received_data = request.data
        serializer = TaskCreateUpdateSerializer(data=received_data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class RetriveUpdateDeleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        # retrive task (task detail)
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskReadSerializer(task, context={'request': request})
        return Response(serializer.data)
    

    def put(self, request, task_id):
        # update task
        return self.update(request, task_id, partial=False)


    def patch(self, request, task_id):
        # update task partially
        return self.update(request, task_id, partial=True)


    def update(self, request, task_id, partial):
        # main task of updating base on partial value which is True for PATCH, False for PUT.
        task = get_object_or_404(Task, id=task_id)
        update_data = request.data
        serializer = TaskCreateUpdateSerializer(instance=task, data=update_data, partial=partial, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


    def delete(self, request, task_id):
        # delete task
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)