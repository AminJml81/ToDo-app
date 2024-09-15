from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ...models import Task
from ..serializers import TaskReadSerializer, TaskCreateEditSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks_list_create(request):
    if request.method == "GET":
        # tasks list
        return list_tasks(request)
    elif request.method == "POST":
        # create task
        return create_task(request)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_retrive_update_delete(request, task_id):
    if request.method == "GET":
        # retrieve task (task detail)
        return retreive_task(request, task_id)
    elif request.method in ("PUT", "PATCH"):
        # update task (partial True for PATCH and False for PUT)
        partial = True if request.method == "PATCH" else True
        return update_task(request, task_id, partial)
    elif request.method == "DELETE":
        # delete task
        return delete_task(request, task_id)


def list_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data)


def create_task(request):
    received_data = request.data
    received_data['user'] = request.user.id
    serializer = TaskCreateEditSerializer(data=received_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def retreive_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    serializer = TaskReadSerializer(task)
    return Response(serializer.data)


def update_task(request, task_id, partial):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    update_data = request.data
    update_data['user'] = request.user.id
    serializer = TaskCreateEditSerializer(instance=task, data=update_data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)