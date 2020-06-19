import unittest
import os
import PIL

from drf_img_resize.settings import TEST_DATA_ROOT
from ..tasks import resize_img


class TestTasksMethods(unittest.TestCase):

    def test_resize_img(self):
        name_image = 'exterior.jpg'
        image_path = os.path.join(TEST_DATA_ROOT, name_image)
        size_like = (1280, 800)
        with PIL.Image.open(image_path) as original_image:
            old_size = original_image.size
            self.assertNotEqual(size_like, old_size)

        res = resize_img.apply(args=(*size_like, image_path, name_image)).get
        self.assertIsNotNone(res)

        with PIL.Image.open(image_path) as original_image:
            cur_size = original_image.size
            self.assertEqual(size_like, cur_size)

        res = resize_img.apply(args=(*old_size, image_path, name_image)).get
        self.assertIsNotNone(res)

        with PIL.Image.open(image_path) as original_image:
            cur_size = original_image.size
            self.assertEqual(old_size, cur_size)
