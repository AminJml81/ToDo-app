from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer


class ListCreateTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # task lists
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskReadSerializer(tasks, many=True, context={'request':request})
        return Response(serializer.data)
    

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