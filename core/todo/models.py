from django.db import models
# from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db import IntegrityError
# Create your models here.

STATUS_CHOICES = (
    ('DO', 'Done'),
    ('TD', 'Todo'),
    ('IP', 'InProgress'),
)    

#user_model = get_user_model()

class Task(models.Model):
    # user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    title = models.CharField(max_length=125)
    description = models.TextField(max_length=255)
    slug = models.SlugField(max_length=150, unique=True, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default= 'TD', choices=STATUS_CHOICES, max_length=2)
    
    # class Meta:
    #     # constraint = models.UniqueConstraint(
    #     #     fields = ['user', 'title', 'created_date'], name='unique_user_task_title_constraint'
    #     # )
    #     ordering = ('-created_date', )

    def get_absolute_url(self):
        return reverse("todo:task-detail", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.title)
        except IntegrityError as e:
            print(e)
        else:
            return super().save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.title
    
