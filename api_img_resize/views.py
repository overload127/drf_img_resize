import os
import redis

from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from celery.result import AsyncResult
from drf_img_resize import settings
from .serializers import TaskCreateSerializer
from .tasks import resize_img, app
from .utilities import get_timestamp_path


# Connect to our Redis instance
redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=1
)

class TaskCreateView(APIView):
    """
    create task and take width height and image
    """
    serializer = TaskCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        create task and take width height and image
        """
        context = dict()
        serializer = TaskCreateSerializer(data=request.data)
        if not serializer.is_valid():
            context = serializer.errors
            context['description'] = 'fail serializer'
            context['status'] = 'FAIL'
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        media_root = settings.IMAGES_ROOT
        if not os.path.exists(media_root):
            os.mkdir(media_root)

        if os.path.isfile(media_root):
            # папка не папка а файл
            context['status'] = 'FAIL'
            context['description'] = 'Can not save the file.' \
                'Folder "images" is a file type'
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        image_name = get_timestamp_path(
            serializer.validated_data['image'].name)
        image_path = os.path.join(media_root, image_name)
        with open(image_path, 'wb+') as fp:
            for chunk in request.FILES['image']:
                fp.write(chunk)

        # run celery task
        task = resize_img.delay(
            serializer.data['width'],
            serializer.data['height'],
            image_path,
            image_name
        )
        redis_instance.setex(
            str(task.id),
            settings.REDIS_STORAGE_TIME,
            1
        )

        context['status'] = 'SUCCESS'
        context['task_id'] = task.id
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
        if not redis_instance.exists(task_id):
            context = dict()
            context['status'] = 'FAIL'
            context['description'] = 'Task not exist'
            return Response(context, status=status.HTTP_200_OK)

        task = AsyncResult(task_id, app=app)
        task_status = task.state

        context = dict()
        context['status'] = 'SUCCESS'
        context['task_id'] = task_id
        context['task_status'] = task_status

        if task_status == 'PENDING':
            context['progress'] = 0
        elif task_status == 'SUCCESS':
            url_image = task.get()
            if not url_image:
                context['status'] = 'FAIL'
                context['description'] = 'do not have url image',

            context['image'] = url_image
            context['progress'] = 100
        elif task_status == 'PROGRESS':
            context['progress'] = task.result.get('progress', None)
        else:
            context['status'] = 'FAIL'
            context['description'] = 'Unknown error'
            context['task_status'] = task_status

        return Response(context, status=status.HTTP_200_OK)


class TaskDeleteView(APIView):
    """
    delete task
    """

    def get(self, request, task_id):
        """
        delete task
        """
        if not redis_instance.exists(task_id):
            context = dict()
            context['status'] = 'FAIL'
            context['description'] = 'Task not exist'
            return Response(context, status=status.HTTP_200_OK)

        redis_instance.delete(task_id)

        task = AsyncResult(task_id, app=app)
        task_status = task.state

        context = dict()
        context['status'] = 'SUCCESS'

        if task_status == 'SUCCESS':
            task.forget()
        else:
            context['status'] = 'FAIL'
            context['description'] = 'Unknown error'
            context['task_status'] = task_status

        return Response(context, status=status.HTTP_200_OK)
