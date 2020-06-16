import os

from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from celery.result import AsyncResult

from drf_img_resize import settings
from .serializers import TaskCreateSerializer
from .tasks import resize_img, app
from .utilities import get_timestamp_path


class TaskCreateView(APIView):
    """
    create task and take width height and image
    """
    serializer = TaskCreateSerializer

    def post(self, request, *args, **kwargs):
        context = dict()
        serializer = TaskCreateSerializer(data=request.data)
        if not serializer.is_valid():
            context = serializer.errors
            context['is_error'] = True
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        media_root = settings.IMAGES_ROOT
        if not os.path.exists(media_root):
            os.mkdir(media_root)

        if os.path.isfile(media_root):
            # папка не папка а файл
            context['is_error'] = True
            context['description'] = 'Не могу сохранить файл.' \
                'Папка является типом файл'
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        image_name = get_timestamp_path(
            serializer.validated_data['image'].name)
        image_path = os.path.join(media_root, image_name)
        with open(image_path, 'wb+') as fp:
            for chunk in request.FILES['image']:
                fp.write(chunk)

        task = resize_img.delay(
            serializer.data['nxt_width'],
            serializer.data['nxt_height'],
            image_path,
            image_name
        )

        context['is_error'] = False
        context['id'] = task.id
        context['status'] = task.status
        return Response(context, status=status.HTTP_201_CREATED)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class TaskCheckView(APIView):
    """
    check completed resize image
    """

    def get(self, request, task_id):
        """
        return status resizing
        """
        task = AsyncResult(task_id, app=app)
        context = dict()
        context['is_error'] = False
        context['task_status'] = task.status
        context['task_id'] = task.id

        if task.state == 'SUCCESS':
            context['results'] = task.get()

        return Response(context, status=status.HTTP_200_OK)
