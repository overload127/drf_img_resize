from django.db import models
from django.core.validators import FileExtensionValidator

from .utilities import get_timestamp_path
from .validators import validate_image_size, validator_image_dpi, validate_image_extension


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
    nxt_width = models.PositiveSmallIntegerField(
        verbose_name='Ширина')
    nxt_height = models.PositiveSmallIntegerField(
        verbose_name='Высота')

    def __str__(self):
        return f'{self.image} - w:{self.nxt_width} - h:{self.nxt_height}'
