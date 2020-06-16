import os

from celery import Celery

# for run celery on windows 10
# celery -A drf_img_resize worker -l info -P eventlet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_img_resize.settings')

app = Celery('drf_img_resize')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
