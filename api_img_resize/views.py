from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from .models import Task
from .serializers import TaskDetailSerializer, ImageSerializer
from rest_framework.response import Response


class TaskCreateView(APIView):
    """Create and send new task id"""
    serializer_class = TaskDetailSerializer

    def post(self, request, *args, **kwargs):
        new_task = Task.objects.create()
        new_task.save()
        serializer = self.serializer_class(new_task)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class AddImageAndDoingTuskView(generics.CreateAPIView):
    """Get image and doing task"""
    serializer_class = ImageSerializer
