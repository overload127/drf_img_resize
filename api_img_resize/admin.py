from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    # fieldsets = (
    #    (None, {'fields': ('id', 'image')}),
    # )
    list_display = ('id', 'status', 'date_created', 'nxt_width', 'nxt_height')
    ordering = ('-date_created',)

    class Meta:
        model = models.Task


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    # fieldsets = (
    #    (None, {'fields': ('id', 'image')}),
    # )
    list_display = ('id', 'task', 'image')

    class Meta:
        model = models.Image
