from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.conf import settings


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
    status = models.CharField(choices=TaskStatusChoices, default='CREATED')
    assigned_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    task_history = HistoricalRecords()

    def __str__(self):
        return self.name


class HistoricalTaskEvent(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    user_who_edited = models.CharField(max_length=100)
    field_to_update = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    old_value = ArrayField(models.TextField(blank=True), blank=True, null=True)
    new_value = ArrayField(models.TextField(blank=True), blank=True, null=True)
    occurrence_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        msg = ' '.join(
            ['value of field %s has been changed from %s to %s by user %s'
             .format(field, old, new) for field, old, new in
             zip(self.field_to_update, self.old_value, self.new_value)]
        )

        return ("Task %s has been modified at %s in the following fields:\n%s"
                .format(self.task.name, self.occurrence_date, msg))
