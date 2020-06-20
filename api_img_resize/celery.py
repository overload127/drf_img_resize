import os

from celery import Celery
from celery.schedules import crontab
#from tasks import cleanup_media_image


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_img_resize.settings')

app = Celery('api_img_resize')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'add-4:00': {
        'task': 'api_img_resize.tasks.cleanup_media_image',
        'schedule': crontab(hour=4, minute=5),
    },
}
