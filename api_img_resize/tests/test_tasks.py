import os
import PIL
import time
import shutil
import unittest
import datetime as dt
from os.path import splitext

from drf_img_resize.settings import TEST_DATA_ROOT, IMAGES_ROOT
from ..tasks import resize_img, cleanup_media_image


class TestTasksMethods(unittest.TestCase):

    def setUp(self):
        self.name_image = 'exterior.jpg'
        self.image_path = os.path.join(TEST_DATA_ROOT, self.name_image)
        old_date_name = dt.datetime.now() - dt.timedelta(days=1)

        self.name_image_temp = '{0}{1}'.format(
            old_date_name.timestamp(), splitext(self.image_path)[1])

        self.image_path_temp = os.path.join(
            IMAGES_ROOT, self.name_image_temp)

    def test_resize_img(self):
        size_like = (1280, 800)
        with PIL.Image.open(self.image_path) as original_image:
            old_size = original_image.size
            self.assertNotEqual(size_like, old_size)

        res = resize_img.apply(
            args=(*size_like, self.image_path, self.name_image)
        ).get()
        self.assertIsNotNone(res)

        with PIL.Image.open(self.image_path) as original_image:
            cur_size = original_image.size
            self.assertEqual(size_like, cur_size)

        res = resize_img.apply(args=(
            *old_size, self.image_path, self.name_image
            )).get
        self.assertIsNotNone(res)

        with PIL.Image.open(self.image_path) as original_image:
            cur_size = original_image.size
            self.assertEqual(old_size, cur_size)

    def test_cleanup_media_image(self):
        try:
            shutil.copy(self.image_path, self.image_path_temp)
        except Exception as err:
            self.fail(
                    'validator_image_dpi() Attempt to make a copy ' /
                    f'failed! {err}'
                )

        file_exist = os.path.exists(self.image_path_temp)
        self.assertTrue(file_exist)

        cleanup_media_image.apply()

        file_exist = os.path.exists(self.image_path_temp)
        self.assertFalse(file_exist)
