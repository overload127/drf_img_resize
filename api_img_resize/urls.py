from django.urls import path
from . import views


app_name = 'api_resize_task'
urlpatterns = [
    path(
        'task/create/',
        views.TaskCreateView.as_view(),
        name='task_create'
    ),
    path(
        'task/check/<str:task_id>/',
        views.TaskCheckView.as_view(),
        name='task_check'
    ),
    path(
        'task/delete/<str:task_id>/',
        views.TaskDeleteView.as_view(),
        name='task_delete'
    ),
]
