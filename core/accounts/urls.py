from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetConfirmView, 
    PasswordResetDoneView, PasswordResetCompleteView
    )

from accounts.views import SignUpView, CustomPasswordChangeView, manage_account_view
from django.urls import reverse_lazy

app_name = 'account'

urlpatterns = [
    path('', manage_account_view, name='manage'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/',
         LogoutView.as_view(template_name = "registration/logout.html"), name='logout'),

    path('password/change/',
          CustomPasswordChangeView.as_view(), name='change-password'),
          
    path('password/reset/',
          PasswordResetView.as_view(success_url=reverse_lazy("account:reset-password-done")), name='reset-password'),
    path('password/reset/done/',
          PasswordResetDoneView.as_view(), name='reset-password-done'),
    path('password/reset/confirm/<uidb64>/<token>/',
          PasswordResetConfirmView.as_view(success_url = reverse_lazy("account:password-reset-complete")), name='reset-password-confirm'),
    path('password/reset/complete/',
          PasswordResetCompleteView.as_view(), name='password-reset-complete' )
]
