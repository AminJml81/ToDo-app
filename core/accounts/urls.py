from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView)

from accounts.views import SignUpView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name = "registration/logout.html"), name='logout')
]
