from django import forms
from .models import Task, TaskFilter, TaskFieldToBeFiltered, HistoryFilter


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_user']


class FilterTaskForm(forms.ModelForm):
    field_to_be_filtered = forms.ChoiceField(choices=TaskFieldToBeFiltered, widget=forms.RadioSelect())

    class Meta:
        model = TaskFilter
        fields = ['phrase_string']


class FilterHistoryForm(forms.ModelForm):
    task_state_till_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = HistoryFilter
        fields = ['task']
