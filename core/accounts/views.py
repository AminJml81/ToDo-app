from django.shortcuts import render
from django.views.generic import CreateView
from accounts.models import User
from django.urls import reverse_lazy
from accounts.forms import SignUpForm
# Create your views here.


class SignUpView(CreateView):
    model = User
    success_url = reverse_lazy('todo:task-list')
    template_name = 'registration/signup.html'
    form_class = SignUpForm
