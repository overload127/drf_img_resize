import os
import uuid
import time

import PIL
from django.db import models
from django.core.files import File
from django.dispatch import receiver
from django.db.models.signals import post_save


from .utilities import get_timestamp_path


class Task(models.Model):
    """Model for resize task"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPLETED_TYPE = (
        (0, 'Ошибка'),
        (1, 'Новый'),
        (2, 'Обрабатывается'),
        (3, 'Успешно завершено'),
    )
    status = models.PositiveSmallIntegerField(choices=COMPLETED_TYPE, default=1)
    date_created = models.DateTimeField(auto_now=True)
    nxt_width = models.PositiveSmallIntegerField()
    nxt_height = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.COMPLETED_TYPE[self.status][1]}, w:{self.nxt_width}, h:{self.nxt_height}'

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            image.delete()
        super().delete(*args, **kwargs)


class Image(models.Model):
    """ All info image """
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Изображение',
    )
    TYPE_IMG = (
        (0, 'Оригинал'),
        (1, 'Измененное')
    )
    type_img = models.PositiveSmallIntegerField(choices=TYPE_IMG, default=0)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Задача')

    def __str__(self):
        return f'{self.image}'


@receiver(post_save, sender=Image, dispatch_uid='resize_img')
def post_save_doing_tusk(sender, **kwargs):
    """func get image and call resize. Next save new image and type in db"""
    image_source = kwargs.get('instance', False)
    if not image_source:
        # обновить в таск статус на ошибкую хрен его знает как если ничего нет
        raise Exception('Error in kwargs["instance"]')
    type_img = image_source.type_img

    if type_img == 1:
        return None

    cur_task = Task.objects.get(id=image_source.task.id)
    cur_task.status = 2
    cur_task.save(update_fields=["status"])

    input_image_path = image_source.image.path
    img_path_split = os.path.split(input_image_path)
    output_image_path = os.path.join(
        img_path_split[0],
        f'resize_{img_path_split[1]}'
    )
    size = (cur_task.nxt_width, cur_task.nxt_height)

    with PIL.Image.open(input_image_path) as original_image:
        width, height = original_image.size
        print(f'The original image size is {width} wide x {height} high')
        # original_image_rgb = original_image.convert('RGB')
        resized_image = original_image.resize(size, PIL.Image.LANCZOS)
        resized_image.save(output_image_path)
        width, height = resized_image.size
        print(f'The resized image size is {width} wide x {height} high')
        resized_image.close()

    # resized_image.save(output_image_path)

    with open(output_image_path, 'rb') as f:
        django_file_img_resize = File(f)
        resize_image_orm = Image()
        resize_image_orm.type_img = 1
        resize_image_orm.task_id = image_source.task.id
        resize_image_orm.image.save(
            img_path_split[1],
            django_file_img_resize,
            save=True
        )

    # Имитируем долго выолняемую задачу
    print('pre')
    time.sleep(20)
    print('post')
    cur_task.status = 3
    cur_task.save(update_fields=['status'])


post_save.connect(post_save_doing_tusk, sender=Image, dispatch_uid='resize_img')


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print(f'The original image size is {width} wide x {height} high')

    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print(f'The resized image size is {width} wide x {height} high')
    resized_image.save(output_image_path)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
