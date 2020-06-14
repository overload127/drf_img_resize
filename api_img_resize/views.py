from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.settings import api_settings
from rest_framework.response import Response

from .models import Task
from .serializers import TaskCreateSerializer, TaskAndImageDetailSerializer, ImageDetailSerializer, TaskDetailSerializer
from rest_framework.response import Response


class TaskCreateView(generics.GenericAPIView):
    """Create and send new task id"""
    serializer_class = TaskCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_task = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'id': new_task.id}, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ImgSendView(generics.CreateAPIView):
    """"""
    serializer_class = ImageDetailSerializer


class TaskCheckView(generics.RetrieveAPIView):
    """check completed resize image"""
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


class ImageGetView(APIView):
    """check completed resize image"""

    def get(self, request, pk):
        data_task = Task.objects.get(id=pk)#, image__type_img=1)# .values('id', 'status', 'image__image')
        serializer = TaskAndImageDetailSerializer(data_task)
        return Response(serializer.data)
