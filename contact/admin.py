from django.contrib import admin
from contact.models import Information, Chat


class InformationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'target_one',
        'target_two',
    )


admin.site.register(Information, InformationAdmin)
admin.site.register(Chat, ChatAdmin)
