from django.contrib import admin
from .models import Target, Topic


class TargetAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'radius',
        'location',
    )


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'photo',
    )


admin.site.register(Target, TargetAdmin)
admin.site.register(Topic, TopicAdmin)
