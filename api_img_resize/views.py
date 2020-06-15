from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .serializers import TaskCreateSerializer, TaskChaeckializer
from .models import Task


class TaskCreateView(APIView):
    """
    check completed resize image
    """
    serializer = TaskCreateSerializer

    def post(self, request, *args, **kwargs):
        # ,{'context': {'request': self.request,'format': self.format_kwarg,'view': self}}
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_task = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'id': new_task.id}, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class TaskCheckView(APIView):
    """
    check completed resize image
    """

    def get(self, request, pk):
        data_task = get_object_or_404(Task, id=pk)
        serializer = TaskChaeckializer(data_task)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
