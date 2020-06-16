from rest_framework import serializers

from api_img_resize.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model
    """

    class Meta:
        model = Task
        fields = ('nxt_width', 'nxt_height', 'image')
