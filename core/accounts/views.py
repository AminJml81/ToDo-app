from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from accounts.models import User
from accounts.forms import SignUpForm


def manage_account_view(request):
    return render(request, 'registration/manage_account.html')


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    success_url = reverse_lazy('todo:task-list')
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_message = "You're registered successfully"


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
     
     success_url = reverse_lazy("account:login")
     success_message = "'Password change successful'"
    