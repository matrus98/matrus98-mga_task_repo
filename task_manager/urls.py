from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/new/', views.task_create_new, name='task_create_new'),
    path('task/<int:pk>', views.task_details, name='task_details'),
    path('task/<int:pk>/edit', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete', views.task_delete, name='task_delete')
]