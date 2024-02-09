from rest_framework import serializers
from task_manager.models import Task, HistoricalTaskEvent


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class HistoricalTaskEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalTaskEvent
        fields = '__all__'
