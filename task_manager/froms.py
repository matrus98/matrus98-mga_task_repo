from django import forms
from .models import Task
from django.contrib.auth import get_user_model


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_user']


def _try_get_users():
    try:
        return list(get_user_model().objects.all())
    except:
        return []

class FilterTaskForm(forms.Form):
    TaskStatusChoices = {
        '': '-----',
        'Nowy': 'Nowy',
        'W toku': 'W toku',
        'Rozwiązany': 'Rozwiązany',
    }


    status = forms.ChoiceField(choices=TaskStatusChoices, required=False)
    assigned_user = forms.ChoiceField(choices=_try_get_users() + [('', '-----')], required=False)
    name_description = forms.CharField(label="Phrase", required=False)


def _get_task_ids_and_names():
    d = {'': '-----'}
    for task in Task.objects.all():
        d[task.id] = task.name
    return d

class FilterHistoryForm(forms.Form):
    task = forms.ChoiceField(choices=_get_task_ids_and_names(), required=False)
    occurrence_date = forms.DateTimeField(
                                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                required=False
                            )
