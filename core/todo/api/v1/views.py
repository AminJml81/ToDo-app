from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateUpdateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_task(request):
    if request.method == "GET":
        # tasks list
        return list_task(request)
    elif request.method == "POST":
        # create task
        return create_task(request)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def retrive_update_delete_task(request, task_id):
    if request.method == "GET":
        # retrieve task (task detail)
        return retreive_task(request, task_id)
    elif request.method in ("PUT", "PATCH"):
        # update task (partial True for PATCH and False for PUT)
        partial = True if request.method == "PATCH" else False
        return update_task(request, task_id, partial)
    elif request.method == "DELETE":
        # delete task
        return delete_task(request, task_id)


def list_task(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskReadSerializer(tasks, many=True, context={'request':request})
    return Response(serializer.data)


def create_task(request):
    received_data = request.data
    serializer = TaskCreateUpdateSerializer(data=received_data,  context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def retreive_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    serializer = TaskReadSerializer(task, context={'request':request})
    return Response(serializer.data)


def update_task(request, task_id, partial):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    update_data = request.data
    serializer = TaskCreateUpdateSerializer(instance=task, data=update_data, partial=partial,  context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)    


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)