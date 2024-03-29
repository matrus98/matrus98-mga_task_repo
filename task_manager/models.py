from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


TaskStatusChoices = {
    'Nowy': 'Nowy',
    'W toku': 'W toku',
    'Rozwiązany': 'Rozwiązany',
}


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100, default='Administrator')
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=TaskStatusChoices, default='Nowy')
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        # return f' Task {self.name} in state {self.status} assigned to {self.assigned_user}'
        return f'{self.name}'


class HistoricalTaskEvent(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True)
    historical_task_id = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    user_who_edited = models.CharField(max_length=100)
    assigned_user = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    fields_to_update = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    old_values = ArrayField(models.TextField(blank=True), blank=True, null=True)
    new_values = ArrayField(models.TextField(blank=True), blank=True, null=True)
    occurrence_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Task {self.task_name} has been modified at: {self.occurrence_date}"
