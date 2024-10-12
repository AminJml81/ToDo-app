from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from todo.models import Task
from django.db.models import Q

# Create your views here.

from todo.forms import TaskForm


class ListTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task-list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user).order_by("-status")
        if q := self.request.GET.get("q"):
            tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))

        return tasks


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "todo/task-detail.html"
    context_object_name = "task"

    def get_queryset(self):
        task = Task.objects.filter(slug=self.kwargs["slug"], user=self.request.user)
        return task


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task-update.html"
    context_object_name = "task"

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user)
        return tasks


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task-create.html"
    success_url = reverse_lazy("todo:task-list")

    def post(self, requets, *args, **kwargs):
        self.object = None
        form = self.get_form()
        form.instance.user = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task-list")

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user)
        return tasks

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
