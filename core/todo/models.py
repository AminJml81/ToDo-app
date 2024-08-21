from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

STATUS_CHOICES = (
    ('DO', 'Done'),
    ('TD', 'Todo'),
    ('IP', 'InProgress'),
)    

user_model = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=125, null=False, blank=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=150, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default= 'TD', choices=STATUS_CHOICES, max_length=2)
    
    class Meta:
        constraints = (models.UniqueConstraint(
            fields = ['user', 'title'], name='unique_user_task_title_constraint'),)


    def get_absolute_url(self):
        return reverse("todo:task-detail", kwargs={"slug": self.slug})


    def __str__(self) -> str:
        return self.title