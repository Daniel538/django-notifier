from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import BulkNotification, Client
from notifications import tasks


@receiver(post_save, sender=BulkNotification, dispatch_uid='schedule_email_notification')
def schedule_notification(**kwargs):
    instance = kwargs['instance']
    data = {
        'pk': instance.pk,
        'updated_at': instance.updated_at
    }
    tasks.prepare_mailing_list.apply_async((), data, eta=instance.start, retry=True)
