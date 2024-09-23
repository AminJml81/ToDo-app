from django.urls import path

from .views import RegistrationGenericView, TokenLoginGenericView

# TODO: Registraion -> Done
#       token authentication:
#             -token/login -> Done
#             -token/logout
#       jwt authentication
#       Account Activation
#       Password reset
#       Password change

app_name = 'api-v1'
urlpatterns = [
    path('registration/', RegistrationGenericView.as_view() , name='registration'),

    path('token/login/', TokenLoginGenericView.as_view(), name='token_login')
]
