from enum import auto

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
import pytz

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


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
    start = models.DateTimeField()
    end = models.DateTimeField()
    filter = models.JSONField(blank=True, null=True)


class Client(TimeStampMixin):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    number = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    code = models.CharField(max_length=10)
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    mails = models.ManyToManyField(
        BulkNotification,
        through='Notification',
        through_fields=('client', 'bulk_mail')
    )


class Notification(TimeStampMixin):
    status = models.CharField(max_length=32, choices=NotificationStatus.choices, default=NotificationStatus.draft)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bulk_mail = models.ForeignKey(BulkNotification, on_delete=models.CASCADE)
