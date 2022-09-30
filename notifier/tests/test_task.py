from functools import partial
from unittest.mock import patch

from notifications.tasks import prepare_mailing_list, send_mail
from notifications import models
from pytest import fixture


@patch('notifications.tasks.send_mail.chunks')
def test_celery_task(chunk_mock, create_clients, bulk_notification):
    default_number = 123
    for i in range(10):
        create_clients(number=default_number + i).save()

    queue_message = {'id': bulk_notification.pk, 'updated_at': bulk_notification.updated_at}
    prepare_mailing_list(queue_message)
    assert bulk_notification.client_set.count() == 10
    chunk_mock.assert_called_once()


def test_send_mail(create_notification):
    # TODO: patch requests API call
    notification = create_notification
    send_mail(notification.client.pk, notification.bulk_mail.pk)
    notification.refresh_from_db()


@fixture
def create_notification(create_clients, bulk_notification):
    client = create_clients()
    client.save()
    bulk_notification.client_set.add(client)
    bulk_notification.save()
    notification = models.Notification.objects.get(client=client.pk, bulk_mail=bulk_notification.pk)
    return notification