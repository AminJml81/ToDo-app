from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers 
        for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password and extra data.
        """

        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(_("Superuser must have is_verified=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User Model for authentication management through email address instead of username
    """
    email = models.EmailField(_("email address"),
                    unique=True,
                    error_messages={
                        "unique": _("A user with that Email already exists."),
                    },)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email