from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from mail_templated import EmailMessage
from threading import Thread
import jwt

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


class EmailThread(Thread):

    def __init__(self, email_template, receiver_email, context):
        super().__init__()
        self.email_obj = EmailMessage()
        self.email_obj.template_name = email_template
        self.email_obj.context = context
        self.email_obj.from_email = 'todo@admin.com'
        self.email_obj.to = receiver_email

    def run(self):
        self.email_obj.send()


def create_token(user):
    token = RefreshToken.for_user(user)
    return str(token.access_token)


def decode_token(token):
    # returns user_id if token is valid
    # raise Validation Error if Invalid
    try:
        decoded_token = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.exceptions.PyJWTError:
        return None

    else:
        # if token is valid, get user_id and return it
        return decoded_token.get('user_id')
    

def send_actvation_email(receiver_email, token):
    template = 'email/user_activation.tpl'
    context = {'token':token, 'user_email':receiver_email}
    email = EmailThread(template, receiver_email=[receiver_email], context=context)
    email.start()