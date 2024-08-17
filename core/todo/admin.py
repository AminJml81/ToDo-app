from django.contrib import admin

# Register your models here.
from todo.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_date')
    list_filter = ('status', )
    date_hierarchy = 'created_date'
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Task, TaskAdmin)