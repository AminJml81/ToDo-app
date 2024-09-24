from rest_framework.serializers import ValidationError

from django.utils.translation import gettext_lazy as _

from ..backends import EmailUsernameBackend



def validate_user(request, username_email, password):
    user = EmailUsernameBackend.authenticate(request=request, username=username_email, password=password)
    if not user:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError({'credentials error':msg}, code='authentication')
    if not user.is_verified:
        msg = _("User is not verified.")
        raise ValidationError({'not verified': msg}, code='verification')
    
    return user