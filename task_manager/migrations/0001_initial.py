# Generated by Django 5.0.1 on 2024-02-02 17:09

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTaskEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=100)),
                ('task_name', models.CharField(max_length=100)),
                ('user_who_edited', models.CharField(max_length=100)),
                ('assigned_user', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=100)),
                ('fields_to_update', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('old_values', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, null=True, size=None)),
                ('new_values', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), blank=True, null=True, size=None)),
                ('occurrence_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TaskFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase_string', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalTask',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('author', models.CharField(default='Administrator', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Nowy', 'Nowy'), ('W toku', 'W toku'), ('Rozwiązany', 'Rozwiązany')], default='CREATED')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assigned_user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical task',
                'verbose_name_plural': 'historical tasks',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(default='Administrator', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Nowy', 'Nowy'), ('W toku', 'W toku'), ('Rozwiązany', 'Rozwiązany')], default='CREATED')),
                ('assigned_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoryFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='task_manager.task')),
            ],
        ),
    ]
