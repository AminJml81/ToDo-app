from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path

from .views import (
    RegistrationGenericView,
    TokenLoginGenericView,
    TokenLogoutGenericView,
    JWTTokenObtainPairView,
    UserActivationConfirmAPIView,
    UserAtivationResendGenericView,
    ChangePasswordGenericView,
    ResetPasswordGenericView,
    ResetPasswordConfirmGenericView,
)

app_name = "api-v1"

urlpatterns = [
    path("registration/", RegistrationGenericView.as_view(), name="registration"),
    path(
        "activation/confirm/<str:token>/",
        UserActivationConfirmAPIView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        UserAtivationResendGenericView.as_view(),
        name="activation-resend",
    ),
    path("token/login/", TokenLoginGenericView.as_view(), name="token-login"),
    path("token/logout/", TokenLogoutGenericView.as_view(), name="token-logout"),
    path("jwt/create/", JWTTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path(
        "change/password/", ChangePasswordGenericView.as_view(), name="change-password"
    ),
    path("reset/password/", ResetPasswordGenericView.as_view(), name="reset-password"),
    path(
        "reset/password/confirm/<str:token>/",
        ResetPasswordConfirmGenericView.as_view(),
        name="reset-password-confirm",
    ),
]
