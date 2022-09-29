from django.contrib import admin

# Register your models here.
from notifications import models


class ClientAdmin(admin.ModelAdmin):
    pass


class BulkNotificationAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.BulkNotification, BulkNotificationAdmin)
admin.site.register(models.Notification, NotificationAdmin)
