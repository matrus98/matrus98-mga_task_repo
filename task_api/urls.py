from django.urls import path, include
from rest_framework import routers

from . import views
from . import views_ModelViewSet
from . import  views_ModelViewSet_History

router = routers.DefaultRouter()
router.register('task', views_ModelViewSet.TaskModelViewSet)
router.register('task/history', views_ModelViewSet_History.HistoryModelViewSet)

urlpatterns = [
    # path('', views.task_list),
    # path('task/new', views.task_create_new),
    # path('task/<int:pk>', views.task_details),
    # path('task/<int:pk>/edit', views.task_edit),
    # path('task/<int:pk>/delete', views.task_delete),
    # path('task/history', views.task_history),
    # path('task/history/<int:pk>/<time>', views.task_history_details),
    path('', include(router.urls))
]
