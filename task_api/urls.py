from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list),
    path('task/new/', views.task_create_new),
    path('task/<int:pk>', views.task_details),
    path('task/<int:pk>/edit', views.task_edit),
    path('task/<int:pk>/delete', views.task_delete),
    path('task/history/', views.task_history),
    path('task/history/<int:pk>/<time>', views.task_history_details),
]