from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    # fieldsets = (
    #    (None, {'fields': ('id', 'image')}),
    # )
    list_display = ('id', 'nxt_width', 'nxt_height', 'status', 'date_created', 'image')
    ordering = ('-date_created',)

    class Meta:
        model = models.Task
