import os

from django.test import TestCase

from api_img_resize.models import Task
from api_img_resize.utilities import get_timestamp_path
from drf_img_resize.settings import TEST_DATA_ROOT
from api_img_resize.validators import (
    validate_image_size, validator_image_dpi, validate_image_extension,
    validate_number_value
)


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Task.objects.create(
            image=os.path.join(TEST_DATA_ROOT, 'exterior.jpg'),
            width=400,
            height=220
        )

    def test_image_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Изображение')

    def test_image_upload_to(self):
        task = Task.objects.get(id=1)
        upload_to = task._meta.get_field('image').upload_to
        self.assertEquals(upload_to, get_timestamp_path)

    def test_image_validators(self):
        task = Task.objects.get(id=1)
        validators_from_class = task._meta.get_field('image').validators
        validators_from_test = [
            validate_image_extension,
            validate_image_size,
            validator_image_dpi,
        ]
        self.assertEquals(validators_from_class, validators_from_test)

    def test_width_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('width').verbose_name
        self.assertEquals(field_label, 'Ширина')

    def test_width_validators(self):
        task = Task.objects.get(id=1)
        validators_from_class = task._meta.get_field('width').validators
        validators_from_test = [
            validate_number_value,
        ]
        self.assertEquals(validators_from_class, validators_from_test)

    def test_height_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('height').verbose_name
        self.assertEquals(field_label, 'Высота')

    def test_height_validators(self):
        task = Task.objects.get(id=1)
        validators_from_class = task._meta.get_field('height').validators
        validators_from_test = [
            validate_number_value,
        ]
        self.assertEquals(validators_from_class, validators_from_test)

    def test_object_str(self):
        task = Task.objects.get(id=1)
        expected_object_name = (
            f'{task.image} - w:{task.width} - h:{task.height}'
        )
        self.assertEquals(expected_object_name, str(task))
