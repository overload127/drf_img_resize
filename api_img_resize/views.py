import os
import redis
import logging

from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

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

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.info(f'start sait')


class TaskCreateView(GenericAPIView):
    """
    Request handler for 'task/create/'
    """
    serializer_class = TaskCreateSerializer

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

            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.warning(f'fail serializer: {log_string}')

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        image_root = settings.IMAGES_ROOT
        if not os.path.exists(image_root):
            logger.warning(f'Create folder for image: image_root={image_root}')
            os.mkdir(image_root)

        if os.path.isfile(image_root):
            # папка не папка а файл
            logger.critical(f'Bad folder for image: image_root={image_root}')
            raise(f'Bad folder for image: image_root={image_root}')

        image_name = get_timestamp_path(
            serializer.validated_data['image'].name)
        image_path = os.path.join(image_root, image_name)
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

        param_list = [f'{key}={value}' for key, value in context.items()]
        log_string = ' '.join(param_list)
        logger.info(f'Create task: {log_string}')

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

            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.warning(f'Task not exist: {log_string}')

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
                context['description'] = 'missing url image',

            context['image'] = url_image
            context['progress'] = 100
        elif task_status == 'PROGRESS':
            context['progress'] = task.result.get('progress', None)
        else:
            context['status'] = 'FAIL'
            context['description'] = 'Unknown error'
            context['task_status'] = task_status

        if context['status'] == 'FAIL':
            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.error(f'{context["description"]}: {log_string}')
        else:
            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.info(f'Check task: {log_string}')

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

            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.warning(f'Task not exist: {log_string}')

            return Response(context, status=status.HTTP_200_OK)

        redis_instance.delete(task_id)

        task = AsyncResult(task_id, app=app)
        task_status = task.state

        context = dict()
        context['status'] = 'SUCCESS'

        if task_status == 'SUCCESS':
            task.forget()

            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.info(f'Task was delete: {log_string}')
        else:
            context['status'] = 'FAIL'
            context['description'] = 'Unknown error'
            context['task_status'] = task_status

            param_list = [f'{key}={value}' for key, value in context.items()]
            log_string = ' '.join(param_list)
            logger.error(f'{context["description"]}: {log_string}')

        return Response(context, status=status.HTTP_200_OK)
