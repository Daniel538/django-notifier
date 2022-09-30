from unittest.mock import patch

from notifications.models import BulkNotification

endpoint = '/api/v1/notifications'


@patch('notifications.signals.tasks')  # don't send celery tasks
def test_e2e_bulk_notification(_, api_client):
    bulk_notification = {
        'message': 'Test message',
        'start': '2021-06-28T17:47:36Z',
        'end': '2021-06-29T17:47:36Z',
    }
    res = api_client.post(f'{endpoint}/bulk-notifications', data=bulk_notification)
    assert res.status_code == 201
    assert BulkNotification.objects.count() == 1
    assert BulkNotification.objects.first().message == bulk_notification['message']

    res = api_client.get(f'{endpoint}/bulk-notifications')
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {**bulk_notification, 'filter': {}}

    _id = BulkNotification.objects.first().pk

    res = api_client.patch(f'{endpoint}/bulk-notifications/{_id}', data={'message': 'Test update'})
    assert res.status_code == 200
    assert BulkNotification.objects.first().message == 'Test update'

    res = api_client.put(f'{endpoint}/bulk-notifications/{_id}', data=bulk_notification)
    assert res.status_code == 200
    assert BulkNotification.objects.first().message == bulk_notification['message']

    res = api_client.delete(f'{endpoint}/bulk-notifications/{_id}')
    assert res.status_code == 204
    assert BulkNotification.objects.count() == 0

