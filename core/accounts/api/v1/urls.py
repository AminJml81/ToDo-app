from django.urls import path

from .views import (
        RegistrationGenericView,
        TokenLoginGenericView,
        TokenLogoutGenericView,
        JWTTokenObtainPairView
) 

# TODO: Registraion -> Done
#       token authentication:
#             -token/login -> Done
#             -token/logout -> Done
#       jwt authentication:
#            -jwt/create/ (create refresh & access token) ->Done
#            -jwt/verify/       
#       Account Activation
#       Password reset
#       Password change

app_name = 'api-v1'

urlpatterns = [
    path('registration/', RegistrationGenericView.as_view() , name='registration'),

    path('token/login/', TokenLoginGenericView.as_view(), name='token-login'),
    path('token/logout/', TokenLogoutGenericView.as_view(), name='token-logout'),

    path('jwt/create/', JWTTokenObtainPairView.as_view(), name='jwt-create'),
]
