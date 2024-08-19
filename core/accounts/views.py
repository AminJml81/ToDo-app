from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

# Create your views here.
from accounts.models import User
from accounts.forms import SignUpForm


def manage_account_view(request):
    return render(request, 'registration/manage_account.html')


class SignUpView(CreateView):
    model = User
    success_url = reverse_lazy('todo:task-list')
    template_name = 'registration/signup.html'
    form_class = SignUpForm

class CustomPasswordChangeView(PasswordChangeView):
     
     success_url = reverse_lazy("account:login")

     def form_valid(self, form):
        messages.success(self.request, 'Password change successful' )
        return super().form_valid(form)
    