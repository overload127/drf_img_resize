import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_img_resize.settings')

app = Celery('api_img_resize')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
