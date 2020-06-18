from django.urls import path
from . import views


app_name = 'api_resize_task'
urlpatterns = [
    path('1/', views.TaskCreateView.as_view()),
    path('2/<str:task_id>/', views.TaskCheckView.as_view()),
    path('3/<str:task_id>/', views.TaskDeleteView.as_view()),
]
