from django import forms
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from todo.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "status"]
        error_messages = {
            "title": {"required": "Title is Required"},
        }

    def clean(self):
        """
        Override the default clean method to check whether this course has
        been already inputted.
        """
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        user = self.instance.user
        slug = slugify(title)
        if not slug:
            raise ValidationError(
                _("Invalid title '%(title)s' !!!"),
                code="invalid",
                params={"title": title},
            )

        user_tasks = Task.objects.filter(user=user)

        if (
            user_tasks.filter(title=title).exists()
            or user_tasks.filter(slug=slug).exists()
        ):
            raise ValidationError(
                _("%(username)s you Have already added '%(title)s'!!!"),
                code="invalid",
                params={"username": user.username, "title": title},
            )

        self.instance.slug = slug
        return self.cleaned_data
