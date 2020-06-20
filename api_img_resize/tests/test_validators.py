import unittest
import PIL
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from drf_img_resize.settings import TEST_DATA_ROOT
from api_img_resize import validators
from api_img_resize.tasks import resize_img


class TestValidateMethods(unittest.TestCase):

    def setUp(self):
        self.name_image = 'exterior.jpg'
        self.image_path = os.path.join(TEST_DATA_ROOT, self.name_image)

    def test_validate_image_size_good(self):
        with open(self.image_path, 'rb') as original_image:
            file_memory = InMemoryUploadedFile(
                original_image, 'image', self.name_image,
                'image', 1000, ''
            )
            try:
                validators.validate_image_size(file_memory)
            except Exception:
                self.fail(
                    'validate_image_size() raised Exception unexpectedly!'
                )

    def test_validate_image_size_bad(self):
        with open(self.image_path, 'rb') as original_image:
            file_memory = InMemoryUploadedFile(
                original_image, 'image', self.name_image,
                'image', 10000000000, ''
            )
            self.assertRaises(
                Exception,
                validators.validate_image_size,
                file_memory
            )

    def test_validator_image_dpi_good(self):
        with open(self.image_path, 'rb') as original_image:
            file_memory = InMemoryUploadedFile(
                original_image, 'image', self.name_image,
                'image', 1000, ''
            )
            try:
                validators.validator_image_dpi(file_memory)
            except Exception:
                self.fail(
                    'validator_image_dpi() raised Exception unexpectedly!'
                )

    def test_validator_image_dpi_width_max_bad(self):
        with PIL.Image.open(self.image_path) as original_image:
            old_size = original_image.size

        resize_img.apply(args=(11300, 2222, self.image_path, self.name_image))

        with open(self.image_path, 'rb') as original_image:
            file_memory = InMemoryUploadedFile(
                original_image, 'image', self.name_image,
                'image', 1000, ''
            )
            self.assertRaises(
                Exception,
                validators.validator_image_dpi,
                file_memory
            )

        resize_img.apply(args=(*old_size, self.image_path, self.name_image))

    def test_validator_image_dpi_height_max_bad(self):
        with PIL.Image.open(self.image_path) as original_image:
            old_size = original_image.size

        resize_img.apply(args=(1300, 23456, self.image_path, self.name_image))

        with open(self.image_path, 'rb') as original_image:
            file_memory = InMemoryUploadedFile(
                original_image, 'image', self.name_image,
                'image', 1000, ''
            )
            self.assertRaises(
                Exception,
                validators.validator_image_dpi,
                file_memory
            )

        resize_img.apply(args=(*old_size, self.image_path, self.name_image))

    def test_validate_image_extension_good(self):
        with open(self.image_path, 'rb') as byte_file, PIL.Image.open(self.image_path) as image_file:
            file_memory = InMemoryUploadedFile(
                byte_file, image_file, self.name_image,
                'image', 1000, ''
            )
            file_memory.image = image_file
            try:
                validators.validate_image_extension(file_memory)
            except Exception:
                self.fail(
                    'validate_image_extension() raised Exception unexpectedly!'
                )

    def test_validate_number_value(self):
        try:
            validators.validate_number_value(2445)
        except Exception:
            self.fail(
                'validate_number_value() raised Exception unexpectedly!'
            )

        self.assertRaises(
            Exception,
            validators.validate_number_value,
            -1934
        )

        self.assertRaises(
            Exception,
            validators.validate_number_value,
            10000
        )
