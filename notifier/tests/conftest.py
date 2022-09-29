from rest_framework.test import APIClient
from pytest import fixture
import django


@fixture
def client():
    return APIClient()


def pytest_sessionstart(session):
    django.setup()


def pytest_sessionfinish(session, exitstatus):
    # clean-up
    from notifications.models import BulkNotification, Client
    BulkNotification.objects.all().delete()
    Client.objects.all().delete()
