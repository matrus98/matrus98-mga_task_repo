import django_filters
from django.db.models import Q
from django import forms
from task_manager.models import Task, HistoricalTaskEvent


class TaskFilter(django_filters.FilterSet):
    name_description = django_filters.rest_framework.CharFilter(method='name_description_filter', label="Phrase")

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'assigned_user': ['exact'],
        }

    def name_description_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )


class HistoricalTaskEventFilter(django_filters.FilterSet):
    occurrence_date = django_filters.DateTimeFilter(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Task state till date',
        lookup_expr='lte',
    )

    class Meta:
        model = HistoricalTaskEvent
        fields = ['task']

    def task_name_filter(self, queryset, name, value):
        return queryset.filter(task_name=value)
