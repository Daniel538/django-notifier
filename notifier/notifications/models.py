from enum import auto

from django.db import models
import pytz


class NotificationStatus(models.IntegerChoices):
    draft = auto()
    success = auto()
    error = auto()


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BulkNotification(TimeStampMixin):
    message = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    filter = models.JSONField()


class Client(TimeStampMixin):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    number = models.IntegerField()
    code = models.CharField(max_length=10)
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    mails = models.ManyToManyField(BulkNotification)


class Notification(TimeStampMixin):
    status = models.CharField(max_length=32, choices=NotificationStatus.choices, default=NotificationStatus.draft)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bulk_mail = models.ForeignKey(BulkNotification, on_delete=models.CASCADE)
