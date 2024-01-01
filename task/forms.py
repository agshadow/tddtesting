from django import forms
from task.models import Task

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = {'title', 'description'}

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = {'title', 'description'}