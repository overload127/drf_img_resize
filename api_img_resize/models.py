from django.db import models

from .utilities import get_timestamp_path
from .validators import (
    validate_image_size, validator_image_dpi, validate_image_extension,
    validate_number_value
)


class Task(models.Model):
    """
    All info of task
    """
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Изображение',
        validators=[
            validate_image_extension,
            validate_image_size,
            validator_image_dpi
        ]
    )
    width = models.PositiveSmallIntegerField(
        verbose_name='Ширина',
        validators=[
            validate_number_value
        ])
    height = models.PositiveSmallIntegerField(
        verbose_name='Высота',
        validators=[
            validate_number_value
        ])

    class Meta:
        verbose_name = 'Задача ресайза'
        verbose_name_plural = 'Задачи ресайза'

    def __str__(self):
        return f'{self.image} - w:{self.width} - h:{self.height}'
