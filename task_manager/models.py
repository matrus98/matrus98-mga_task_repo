from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
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
    status = models.CharField(choices=TaskStatusChoices, default='CREATED')
    assigned_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    task_history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}, {self.status}, {self.assigned_user}'


class HistoricalTaskEvent(models.Model):
    task_id = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    user_who_edited = models.CharField(max_length=100)
    assigned_user = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    fields_to_update = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    old_values = ArrayField(models.TextField(blank=True), blank=True, null=True)
    new_values = ArrayField(models.TextField(blank=True), blank=True, null=True)
    occurrence_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        msg = ' '.join(
            ['value of field %s has been changed from %s to %s by user %s'
             .format(field, old, new) for field, old, new in
             zip(self.fields_to_update, self.old_values, self.new_values)]
        )

        return ("Task %s has been modified at %s in the following fields:\n%s"
                .format(self.task_name, self.occurrence_date, msg))


TaskFieldToBeFiltered = {
    'none': 'Do not filter',
    'name_description': 'Task name and description',
    'status': 'Task Status',
    'assigned_user': 'Assigned user',
}


class TaskFilter(models.Model):
    phrase_string = models.CharField(max_length=100)

    def __str__(self):
        return 'Filter for phrase: %s' % self.phrase_string
