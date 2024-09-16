from django_filters import rest_framework as filters

from ..models import Task


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.TaskStatus.choices
                                  )
    class Meta:
        model = Task
        fields = {
            'title': ['icontains'],
            'description': ['icontains'], 
        }
