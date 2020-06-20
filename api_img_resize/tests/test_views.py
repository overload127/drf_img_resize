import os
import uuid
import time

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from drf_img_resize.settings import TEST_DATA_ROOT


class TaskCreateTestCase(APITestCase):

    def test_taskcreate(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 333, 'height': 222,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.post(url, data, format='multipart')
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['status'], 'SUCCESS')
            self.assertIsNotNone(response.data['task_id'])

    def test_taskcreate_bad_get(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 333, 'height': 222,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.get(url, data, format='multipart')
            self.assertEquals(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_taskcreate_bad_width(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 44444, 'height': 222,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.post(url, data, format='multipart')
            self.assertEquals(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )
            self.assertEqual(response.data['status'], 'FAIL')
            self.assertEqual(response.data['description'], 'fail serializer')

    def test_taskcreate_bad_height(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 333, 'height': 44444,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.post(url, data, format='multipart')
            self.assertEquals(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )
            self.assertEqual(response.data['status'], 'FAIL')
            self.assertEqual(response.data['description'], 'fail serializer')

    def test_taskcreate_bad_file(self):
        data = {'width': 333, 'height': 222,
                'image': ''}
        url = reverse('api_resize_task:task_create')
        response = self.client.post(url, data, format='multipart')
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(response.data['status'], 'FAIL')
        self.assertEqual(response.data['description'], 'fail serializer')


class TaskCheckTestCase(APITestCase):

    def setUp(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 333, 'height': 222,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.post(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.task_id = response.data['task_id']

    def test_taskcheck(self):
        time.sleep(1)
        url = reverse('api_resize_task:task_check', args=(self.task_id,))
        data = {}
        response = self.client.get(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_taskcheck_bad_post(self):
        url = reverse('api_resize_task:task_check', args=(self.task_id,))
        data = {}
        response = self.client.post(url, data, format='multipart')

        self.assertEquals(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_taskcheck_bad_uuid(self):
        url = reverse('api_resize_task:task_check', args=(uuid.uuid4(),))
        data = {}
        response = self.client.get(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'FAIL')
        self.assertEqual(response.data['description'], 'Task not exist')


class TaskDeleteTestCase(APITestCase):

    def setUp(self):
        with open(
            os.path.join(TEST_DATA_ROOT, 'exterior.jpg'), 'rb'
        ) as data_image:
            data = {'width': 333, 'height': 222,
                    'image': data_image}
            url = reverse('api_resize_task:task_create')
            response = self.client.post(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.task_id = response.data['task_id']

    def test_taskdelete(self):
        time.sleep(10)
        url = reverse('api_resize_task:task_delete', args=(self.task_id,))
        data = {}
        response = self.client.get(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_taskdelete_bad_post(self):
        time.sleep(1)
        url = reverse('api_resize_task:task_delete', args=(self.task_id,))
        data = {}
        response = self.client.post(url, data, format='multipart')

        self.assertEquals(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_taskdelete_bad_uuid(self):
        url = reverse('api_resize_task:task_delete', args=(uuid.uuid4(),))
        data = {}
        response = self.client.get(url, data, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'FAIL')
        self.assertEqual(response.data['description'], 'Task not exist')
