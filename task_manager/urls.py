from django.urls import path, include
from . import views
from . import views_requests

use_requests = False

if use_requests:
    urlpatterns = [
        path('', views_requests.task_list, name='task_list'),
        path('task/new/', views_requests.task_create_new, name='task_create_new'),
        path('task/<int:pk>', views_requests.task_details, name='task_details'),
        path('task/<int:pk>/edit', views_requests.task_edit, name='task_edit'),
        path('task/<int:pk>/delete', views_requests.task_delete, name='task_delete'),
        path('task/history/', views_requests.task_history, name='task_history'),
        path('task/history/<int:pk>/<time>', views_requests.task_history_details, name='task_history_details'),
    ]

else:
    urlpatterns = [
        path('', views.task_list, name='task_list'),
        path('task/new/', views.task_create_new, name='task_create_new'),
        path('task/<int:pk>', views.task_details, name='task_details'),
        path('task/<int:pk>/edit', views.task_edit, name='task_edit'),
        path('task/<int:pk>/delete', views.task_delete, name='task_delete'),
        path('task/history/', views.task_history, name='task_history'),
        path('task/history/<int:pk>/<time>', views.task_history_details, name='task_history_details'),
    ]
