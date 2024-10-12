from django.contrib import admin

# Register your models here.
from todo.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "created_date", "slug")
    list_filter = ("status",)
    search_fields = ("title",)
    date_hierarchy = "created_date"
    prepopulated_fields = {"slug": ("title",)}
