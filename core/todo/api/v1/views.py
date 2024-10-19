from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ...models import Task
from ..pagination import CustomPagination
from ..serializers import TaskReadSerializer, TaskCreateSerializer, TaskUpdateSerializer


@api_view(["GET", "POST"])
def list_create_task(request):
    if request.method == "GET":
        # list tasks
        tasks = list_task(request)
        return Response(tasks)

    elif request.method == "POST":
        # create task
        response = create_task(request)
        if response.status_code == 201:
            cache.delete(f"{request.user}--tasks")
        return response


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def retrive_update_delete_task(request, slug):
    if request.method == "GET":
        # retrieve task (task detail)
        return retreive_task(request, slug)

    elif request.method in ("PUT", "PATCH"):
        # update task (partial True for PATCH and False for PUT)
        partial = True if request.method == "PATCH" else False
        response = update_task(request, slug, partial)
        if response.status_code == 200:
            # delete tasks cache, if some task were updated successfully.
            cache.delete(f"{request.user}--tasks")
        return response

    elif request.method == "DELETE":
        # delete task
        response = delete_task(request, slug)
        if response.status_code == 204:
            # delete tasks cache, if some task were deleted successfully.
            cache.delete(f"{request.user}--tasks")
        return response


def list_task(request):
    paginator = CustomPagination()
    user = request.user
    tasks = cache.get_or_set(
        f"{request.user}--tasks",
        Task.objects.filter(user=user),
        timeout=5 * 60,
    )
    filtered_tasks = filter_tasks(request, tasks)
    filtered_tasks = search_tasks(request, filtered_tasks)
    tasks_page = paginator.paginate_queryset(filtered_tasks, request)
    serializer = TaskReadSerializer(tasks_page, many=True, context={"request": request})
    return serializer.data


def filter_tasks(request, tasks):
    # getting status query parameter and filter the tasks
    status = request.query_params.get("status")
    if status:
        tasks = tasks.filter(status=status)
    return tasks


def search_tasks(request, tasks):
    # getting search query parameter and filter the tasks based on
    # title or description with icontains lookup
    search_key = request.query_params.get("search")
    if search_key:
        tasks = tasks.filter(
            Q(title__icontains=search_key) | Q(description__icontains=search_key)
        )
    return tasks


def create_task(request):
    received_data = request.data
    serializer = TaskCreateSerializer(data=received_data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def retreive_task(request, slug):
    user = request.user
    task = get_object_or_404(Task, slug=slug, user=user)
    serializer = TaskReadSerializer(task, context={"request": request})
    return Response(serializer.data)


def update_task(request, slug, partial):
    user = request.user
    task = get_object_or_404(Task, slug=slug, user=user)
    update_data = request.data
    serializer = TaskUpdateSerializer(
        instance=task, data=update_data, partial=partial, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, headers={"Location": task.get_absolute_url()})


def delete_task(request, slug):
    user = request.user
    task = get_object_or_404(Task, slug=slug, user=user)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
