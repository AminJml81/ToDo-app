from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..pagination import CustomPagination
from ...models import Task
from ..serializers import(
                        TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer
                        )


class ListCreateTaskAPIView(APIView):

    def get(self, request):
        # task lists
        paginator = CustomPagination()
        user = request.user
        tasks = Task.objects.filter(user=user)
        filtered_tasks = self.filter_tasks(request, tasks)
        filtered_tasks = self.search_tasks(request, filtered_tasks)
        tasks_page = paginator.paginate_queryset(filtered_tasks, request)
        serializer = TaskReadSerializer(tasks_page, many=True,
                                         context={'request':request})
        return Response(serializer.data)
    

    def filter_tasks(self, request, tasks):
        # getting status query parameter and filter the tasks
        status = request.query_params.get('status')
        if status:
            tasks = tasks.filter(status=status)
        return tasks
    
    def search_tasks(self, request, tasks):
        # getting search query parameter and filter the tasks based on
        # title or description with icontains lookup
        search_key = request.query_params.get('search')
        if search_key:
            tasks = tasks.filter(Q(title__icontains=search_key) |
                                Q(description__icontains=search_key))
        return tasks
    
    def post(self, request):
        # create new task
        received_data = request.data
        serializer = TaskCreateSerializer(data=received_data, 
                                        context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class RetriveUpdateDeleteTaskAPIView(APIView):
    
    def get(self, request, slug):
        # retrive task (task detail)
        user = request.user
        task = get_object_or_404(Task, user=user, slug=slug)
        serializer = TaskReadSerializer(task, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, slug):
        # update task
        return self.update(request, slug, partial=False)

    def patch(self, request, slug):
        # update task partially
        return self.update(request, slug, partial=True)

    def update(self, request, slug, partial):
        # main task of updating base on partial value 
        # which is True for PATCH, False for PUT.
        user = self.request.user
        task = get_object_or_404(Task, slug=slug, user=user)
        update_data = request.data
        serializer = TaskUpdateSerializer(instance=task, data=update_data,
                                    partial=partial, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, slug):
        # delete task
        user = request.user
        task = get_object_or_404(Task, slug=slug, user=user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)