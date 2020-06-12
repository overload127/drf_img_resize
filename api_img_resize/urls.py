from django.urls import path
from api_img_resize import views


app_name = 'task'
urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('add_img/', views.AddImageAndDoingTuskView.as_view(), name='add_and_due'),
    # path('check_task/', views.CompletedTaskViewSet),
]
