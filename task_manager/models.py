from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings


TaskStatusChoices = {
    'CREATED': 'Nowy',
    'IN_PROGRESS': 'W toku',
    'SOLVED': 'Rozwiązany',
}


class Task(models.Model):
    author = models.CharField(max_length=100, default='Administrator')
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=TaskStatusChoices, default='CREATED')

    # user_choice = {}
    # for username in [user.username for user in User.objects.all()]:
    #     user_choice[username] = username
    # assigned_user = models.CharField(choices=user_choice, blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    task_history = HistoricalRecords()
    # task_detailed_history = []

    def __str__(self):
        return self.name


class HistoricalEvent(models.Model):
    task_name = models.CharField(max_length=100)
    user_choice = {}
    for username in [user.username for user in User.objects.all()]:
        user_choice[username] = username
    user_who_edited = models.CharField(choices=user_choice, blank=True)
    field_to_update = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    def __str__(self):
        return 'LOREM IPSUM'
