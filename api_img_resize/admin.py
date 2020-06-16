from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nxt_width', 'nxt_height', 'image')

    class Meta:
        model = models.Task
