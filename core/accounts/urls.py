from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    )

from accounts.views import SignUpView, CustomPasswordChangeView, manage_account_view
from django.urls import reverse_lazy

app_name = 'account'

urlpatterns = [
    path('', manage_account_view, name='manage'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name = "registration/logout.html"), name='logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='change-password'),
]
