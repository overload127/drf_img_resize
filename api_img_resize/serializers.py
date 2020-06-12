from rest_framework import serializers

from api_img_resize.models import Task, Image


class TaskDetailSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    # image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Task
        fields = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for Image model"""
    # image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        fields = ('source_image', 'nxt_width', 'nxt_height', 'task')
