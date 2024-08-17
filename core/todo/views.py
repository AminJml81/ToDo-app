from django.views.generic import (ListView, DetailView, UpdateView, CreateView, DeleteView)
from django.urls import reverse_lazy
from todo.models import Task

# Create your views here.

from todo.forms import TaskForm


class ListTasksView(ListView):
    model = Task
    template_name = 'task-list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.order_by('status')
        return tasks


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task-detail.html'
    context_object_name = 'task'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task-update.html'
    context_object_name = 'task'
    

class CreateTaskView(CreateView):
    model = Task
    form_class = TaskForm 
    template_name = 'task-create.html'
    success_url = reverse_lazy('todo:task-list')


class DeleteTaskView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('todo:task-list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    