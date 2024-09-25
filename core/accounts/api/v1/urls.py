from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path

from .views import (
        RegistrationGenericView,
        TokenLoginGenericView,
        TokenLogoutGenericView,
        JWTTokenObtainPairView,
        UserActivationConfirmApiView
) 

# TODO: Registraion -> Done
#       token authentication:
#             -token/login -> Done
#             -token/logout -> Done
#       jwt authentication:
#            -jwt/create/ (create refresh & access token) ->Done
#            -jwt/refresh/ (creates another access token if given access is valid) -> Done
#            -jwt/verify/ verifies jwt token -> Done
#       Account Activation
#            -activation/confirm -> Done
#            -activation/resend
#       Password reset
#       Password change

app_name = 'api-v1'

urlpatterns = [
    path('registration/', RegistrationGenericView.as_view() , name='registration'),
    path('activation/confirm/<str:token>/', UserActivationConfirmApiView.as_view(), name='activation'),

    path('token/login/', TokenLoginGenericView.as_view(), name='token-login'),
    path('token/logout/', TokenLogoutGenericView.as_view(), name='token-logout'),

    path('jwt/create/', JWTTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token-verify'),
]