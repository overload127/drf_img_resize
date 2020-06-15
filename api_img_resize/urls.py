from django.urls import path
from . import views


app_name = 'task'
urlpatterns = [
    path('1/', views.TaskCreateView.as_view()),
    path('2/<uuid:pk>/', views.TaskCheckView.as_view()),
]