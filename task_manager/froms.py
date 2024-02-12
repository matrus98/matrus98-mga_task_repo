from django import forms
from .models import Task
from django.contrib.auth import get_user_model


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_user']


def _try_get_users():
    try:
        d = {'': '-----'}
        for user in get_user_model().objects.all():
            d[user.username] = user.username
        return d
    except:  # model does not exist before migration, so if I want perform it it cause error
        return []

class FilterTaskForm(forms.Form):
    TaskStatusChoices = {
        '': '-----',
        'Nowy': 'Nowy',
        'W toku': 'W toku',
        'Rozwiązany': 'Rozwiązany',
    }


    status = forms.ChoiceField(choices=TaskStatusChoices, required=False)
    assigned_user = forms.ChoiceField(choices=_try_get_users(), required=False)
    name_description = forms.CharField(label="Phrase", required=False)


def _get_task_ids_and_names():
    d = {'': '-----'}
    try:
        for task in Task.objects.all():
            d[task.id] = task.name
    except:  # model does not exist before migration, so if I want perform it it cause error
        pass
    return d


class FilterHistoryForm(forms.Form):
    historical_task_id = forms.ChoiceField(choices=_get_task_ids_and_names(), required=False, label='Task')
    occurrence_date = forms.DateTimeField(
                                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                required=False
                            )
