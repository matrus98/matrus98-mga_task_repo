from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .serializers import HistoricalTaskEventSerializer
from .filters import HistoricalTaskEventFilter
from task_manager.models import HistoricalTaskEvent


class HistoryModelViewSet(ModelViewSet):
    queryset = HistoricalTaskEvent.objects.all()
    serializer_class = HistoricalTaskEventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HistoricalTaskEventFilter
