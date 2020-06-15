from rest_framework import serializers

from api_img_resize.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    class Meta:
        model = Task
        fields = ('nxt_width', 'nxt_height', 'image')


class TaskChaeckializer(serializers.ModelSerializer):
    """Serializer for Image model"""

    class Meta:
        model = Task
        fields = ('id', 'status', 'image')
