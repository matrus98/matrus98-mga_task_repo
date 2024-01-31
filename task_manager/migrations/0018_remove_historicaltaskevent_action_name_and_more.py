# Generated by Django 5.0.1 on 2024-01-31 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0017_alter_historicaltaskevent_action_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltaskevent',
            name='action_name',
        ),
        migrations.AddField(
            model_name='historicaltaskevent',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='task_manager.task'),
        ),
    ]
