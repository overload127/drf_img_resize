from django.urls import path
from api_img_resize import views


app_name = 'task'
urlpatterns = [
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/send/img/', views.ImgSendView.as_view(), name='task_send_img'),
    path('task/check/<uuid:pk>/', views.TaskCheckView.as_view(), name='task_check'),
    path('image/get/<uuid:pk>/', views.ImageGetView.as_view(), name='image_get'),
]
