from rest_framework import serializers

from api_img_resize.models import Task, Image


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    class Meta:
        model = Task
        fields = ('nxt_width', 'nxt_height')


class ImageDetailSerializer(serializers.ModelSerializer):
    """Serializer for Image model"""

    class Meta:
        model = Image
        fields = ('image', 'task')


class TaskDetailSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    class Meta:
        model = Task
        fields = ('id', 'status')


class ImageSuccesSerializer(serializers.ModelSerializer):
    """Serializer for Image model"""

    class Meta:
        model = Image
        fields = ('image', 'type_img')


class TaskAndImageDetailSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    images = ImageSuccesSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        #fields = '__all__'
        fields = ('id', 'status', 'images')
