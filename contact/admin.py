from django.contrib import admin
from contact.models import Information


class InformationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Information, InformationAdmin)
