import itertools
import random

from main.celery import app
from notifications import models


@app.task(bind=True)
def prepare_mailing_list(self, *args, chunk_size=100, **kwargs):
    notification = models.BulkNotification.objects.filter(**kwargs).first()
    if notification:
        clients = models.Client.objects.filter(**notification.filter).values_list('id', flat=True)
        # TODO: all client ids in memory
        notification.client_set.add(*clients)
        notification.save()
        send_mail.chunks(zip(clients, itertools.repeat(notification.pk)), chunk_size).apply_async(
            retry=True,
            retry_policy={
                'max_retries': 3,
                'interval_start': 0,
                'interval_step': 0.2,
                'interval_max': 0.2,
            })


@app.task(bind=True)
def send_mail(self, client_id, mail_id, *args, **kwargs):
    message = models.Notification.objects.filter(client=client_id, bulk_mail=mail_id).first()
    if message:
        # TODO call to API
        # requests.post(endpoint, headers=headers, data, timeout)
        status = random.choice([200, 500])
        if status == 200:
            message.status = models.NotificationStatus.success
        elif self.request.retries == self.max_retries:
            message.status = models.NotificationStatus.error
        message.save()
