from django.urls import path

from .views import RegistrationGenericView, TokenLoginGenericView, TokenLogoutGenericView

# TODO: Registraion -> Done
#       token authentication:
#             -token/login -> Done
#             -token/logout -> Done
#       jwt authentication
#       Account Activation
#       Password reset
#       Password change

app_name = 'api-v1'
urlpatterns = [
    path('registration/', RegistrationGenericView.as_view() , name='registration'),

    path('token/login/', TokenLoginGenericView.as_view(), name='token-login'),
    path('token/logout/', TokenLogoutGenericView.as_view(), name='token-logout'),
]
