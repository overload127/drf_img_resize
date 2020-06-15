import os
import uuid
import time

import PIL
from django.db import models
from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_save
from drf_img_resize.celery import app

from .utilities import get_timestamp_path


class Task(models.Model):
    """
    All info of task
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Изображение',
    )
    nxt_width = models.PositiveSmallIntegerField()
    nxt_height = models.PositiveSmallIntegerField()
    COMPLETED_TYPE = (
        (0, 'Ошибка'),
        (1, 'Новый'),
        (2, 'Обрабатывается'),
        (3, 'Успешно завершено'),
    )
    status = models.PositiveSmallIntegerField(choices=COMPLETED_TYPE,
                                              default=1)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.image} {self.status}'

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        if not self.image:
            return None

        if self.status == 1:
            # resize_img.delay(self)
            cur_task = resize_img2.delay(self.nxt_width, self.nxt_height, self.image.path)
            cur_task=cur_task


@app.task
def resize_img2(nxt_width, nxt_height, image_path):
    size = (nxt_width, nxt_height)

    # Открываем через PIL наше изображение
    # И выполняем масштабирование
    with PIL.Image.open(image_path) as original_image:
        width, height = original_image.size
        print(f'The original image size is {width} wide x {height} high')
        original_image = original_image.resize(size, PIL.Image.LANCZOS)
        width, height = original_image.size
        print(f'The resized image size is {width} wide x {height} high')
        original_image.save(image_path)
        original_image.close()

    print('pre')
    time.sleep(2)
    print('post')


#@app.task
def resize_img(cur_task):
    # устанавливаем таску статус обработки
    cur_task.status = 2
    cur_task.save(update_fields=['status'])

    size = (cur_task.nxt_width, cur_task.nxt_height)

    # Открываем через PIL наше изображение
    # И выполняем масштабирование
    with PIL.Image.open(cur_task.image) as original_image:
        width, height = original_image.size
        print(f'The original image size is {width} wide x {height} high')
        original_image = original_image.resize(size, PIL.Image.LANCZOS)
        width, height = original_image.size
        print(f'The resized image size is {width} wide x {height} high')
        original_image.save(cur_task.image.path)
        original_image.close()

    print('pre')
    time.sleep(20)
    print('post')
    # устанавливаем таску статус обработки
    cur_task.status = 3
    cur_task.save(update_fields=['status'])


@receiver(models.signals.post_delete, sender=Task)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
