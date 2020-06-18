from django.urls import path
from . import views


app_name = 'api_resize_task'
urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view()),
    path('task/check/<str:task_id>/', views.TaskCheckView.as_view()),
    path('task/delete/<str:task_id>/', views.TaskDeleteView.as_view()),
]
