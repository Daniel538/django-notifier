from functools import partial

from rest_framework.test import APIClient
from pytest import fixture
import django


@fixture
def api_client():
    return APIClient()


def pytest_sessionstart(session):
    django.setup()


@fixture(scope='module', autouse=True)
def clean_up():
    from notifications.models import BulkNotification, Client
    BulkNotification.objects.all().delete()
    Client.objects.all().delete()

@fixture
def create_clients():
    from notifications import models
    return partial(
        models.Client,
        number=123456789,
        code='37529',
        tag='test',
        timezone='Europe/Luxembourg'
    )


@fixture
def bulk_notification():
    from notifications import models
    notification = models.BulkNotification(
        message='Test message',
        start='2021-06-28T17:47:36Z',
        end='2021-06-29T17:47:36Z',
        filter={'tag': 'test'}
    )
    notification.save()
    return notification
