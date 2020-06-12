import uuid
import shutil
import os

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
        return f'{self.id} {self.status}'


class Image(models.Model):
    """ All info image """
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Изображение',
    )
    TYPE_IMG = (
        (1, 'Оригинальное изображение'),
        (2, 'Масштабируемое изображение')
    )
    type_img = models.PositiveSmallIntegerField(choices=TYPE_IMG)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        verbose_name='Задача')

    def __str__(self):
        return f'{self.image}'


@receiver(post_save, sender=Image, dispatch_uid='resize_img')
def post_save_doing_tusk(sender, **kwargs):
    image_source = kwargs.get('instance', False)
    if not image_source:
        # обновить в таск статус на ошибкую хрен его знает как если ничего нет....
        raise Exception('Error in kwargs["instance"]')
    type_img = image_source.type_img

    if type_img == 2:
        return None

    Task.objects.filter(id=image_source.task.id).update(status=2)

    post_save.disconnect(post_save_doing_tusk, sender=Image, dispatch_uid='resize_img')
    # Внимание, не дай бох тут произойдет какаянидь зхрень, то нужно заново зарегать событие пост сайв...
    img_path = image_source.image.path
    img_path_split = os.path.split(img_path)
    new_path = os.path.join(img_path_split[0], f'resize_{img_path_split[1]}')
    shutil.copyfile(img_path, new_path)

    with open(new_path, 'rb') as file_img_resize:
        django_file_img_resize = File(file_img_resize)
        resize_image = Image()
        resize_image.image = django_file_img_resize
        resize_image.type_img = 2
        resize_image.task_id = image_source.task.id
        resize_image.save()

    Task.objects.filter(id=image_source.task.id).update(status=3)


post_save.connect(post_save_doing_tusk, sender=Image, dispatch_uid='resize_img')


# post_save.connect(post_save_dispatcher, sender=Image)
