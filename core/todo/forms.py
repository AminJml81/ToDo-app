from typing import Any
from django import forms
from django.forms import ValidationError

from todo.models import Task
class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

    
    # def __init__(self, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)
        #print(dir(self.fields['title']))
        # for field_name, field in self.fields.items():
        #     self.fields[field_name].widget.attrs['placeholder'] = field
            #print(field)


    def clean(self) -> dict[str, Any]:
        """ 
        Override the default clean method to check whether this course has
        been already inputted.
        """
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        matching_titles = Task.objects.filter(title=title)
        if self.instance:
            matching_titles = matching_titles.exclude(pk=self.instance.pk)
        if matching_titles.exists():
            message = f"You Have already added '{title}'!!!"
            raise forms.ValidationError(message)
        else:
            return self.cleaned_data
        
