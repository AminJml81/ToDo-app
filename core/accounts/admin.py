from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    model = User
    list_display = ("email", "username", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "username", "is_superuser", "is_active", "is_verified")
    searching_fields = (
        "username",
        "email",
    )
    ordering = (
        "username",
        "email",
    )
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("username", "email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
