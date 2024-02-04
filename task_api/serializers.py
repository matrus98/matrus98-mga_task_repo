from rest_framework import serializers
from task_manager.models import Task, HistoricalTaskEvent, TaskFilter, HistoryFilter


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class HistoricalTaskEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalTaskEvent
        fields = '__all__'


class TaskFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFilter
        fields = '__all__'


class HistoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryFilter
        fields = '__all__'

