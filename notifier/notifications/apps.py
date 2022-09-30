from django.apps import AppConfig
from django.core.signals import request_finished


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from notifications import signals
