import random

from pytest import fixture

from notifications.models import NotificationStatus

endpoint = '/api/v1/notifications'


def test_stats(api_client, create_clients, bulk_notification):
    for i in range(20):
        status = random.choice(NotificationStatus.values)
        client = create_clients(number=i)
        client.save()
        bulk_notification.client_set.add(client, through_defaults={'status': status})
    bulk_notification.save()

    res = api_client.get(f'{endpoint}/stats/{bulk_notification.pk}')
    assert res.status_code == 200
    assert res.data['id'] == bulk_notification.pk
    assert res.data['message'] == bulk_notification.message
    assert 'stats' in res.data.keys()
    assert 'success' in res.data['stats'].keys()
    assert 'error' in res.data['stats'].keys()
    assert 'daft' in res.data['stats'].keys()

