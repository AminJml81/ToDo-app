from rest_framework.serializers import ValidationError
from rest_framework.serializers import ValidationError

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from mail_templated import EmailMessage

from threading import Thread
import jwt
from datetime import datetime, timedelta, timezone

from ..backends import EmailUsernameBackend


class EmailThread(Thread):

    def __init__(self, email_template, receiver_email, context):
        super().__init__()
        self.email_obj = EmailMessage()
        self.email_obj.template_name = email_template
        self.email_obj.context = context
        self.email_obj.from_email = "todo@admin.com"
        self.email_obj.to = receiver_email

    def run(self):
        self.email_obj.send()


def send_email(template, receiver_email, token):
    context = {"token": token, "user_email": receiver_email}
    email = EmailThread(template, receiver_email=[receiver_email], context=context)
    email.start()


def validate_user(request, username_email, password):
    user = EmailUsernameBackend.authenticate(
        request=request, username=username_email, password=password
    )
    if not user:
        msg = _("Unable to log in with provided credentials.")
        raise ValidationError({"credentials error": msg}, code="authentication")
    if not user.is_verified:
        msg = _("User is not verified.")
        raise ValidationError({"not verified": msg}, code="verification")

    return user


def validate_new_passwords(password1, password2):
    # it checks if they match and if new password is strong enough.
    if password1 != password2:
        raise ValidationError({"new passwords": "new passwords don't match"})
    try:
        validate_password(password1)
    except ValidationError as e:
        raise ValidationError({"new password": list(e.messages)})


def create_token(lookup_field, value):
    payload = {
        lookup_field: value,
        "exp": (datetime.now() + timedelta(hours=24)),
        "iat": datetime.now(timezone.utc).timestamp(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return token


def decode_token(token, lookup_field):
    # returns lookup_field if token is valid
    # raise Validation Error if Invalid
    try:
        decoded_token = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.exceptions.PyJWTError:
        return None
    else:
        # if token is valid, get lookup_field and returns it.
        return decoded_token.get(lookup_field)
