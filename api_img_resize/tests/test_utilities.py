import unittest

from api_img_resize.utilities import get_timestamp_path


class TestUtilitiesMethods(unittest.TestCase):

    def test_get_timestamp_path(self):
        name_image = 'new_name.png'
        time_name = get_timestamp_path(name_image)
        self.assertIsNotNone(time_name)
        parts = time_name.split('.')
        self.assertEquals(True, parts[-1].lower() in ['png', 'jpg'])
