from django.urls import path

from .views import RegistrationGenericView

# TODO: Registraion -> Done
#       token authentication
#       jwt authentication
#       Account Activation
#       Password reset
#       Password change
urlpatterns = [
    path('registration/', RegistrationGenericView.as_view() , name='registration')
]
