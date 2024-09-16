from django_filters import rest_framework as filters

from ..models import Task


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.TaskStatus.choices)
