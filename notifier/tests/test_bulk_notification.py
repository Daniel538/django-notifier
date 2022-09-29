from notifications.models import BulkNotification

endpoint = '/api/v1/notifications'


def test_e2e_bulk_notification(client):
    bulk_notification = {
        'message': 'Test message',
        'start': '2021-06-28T17:47:36Z',
        'end': '2021-06-29T17:47:36Z',
    }
    res = client.post(f'{endpoint}/bulk-notifications', data=bulk_notification)
    assert res.status_code == 201
    assert BulkNotification.objects.count() == 1
    assert BulkNotification.objects.first().message == bulk_notification['message']

    res = client.get(f'{endpoint}/bulk-notifications')
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {**bulk_notification, 'filter': None}

    _id = BulkNotification.objects.first().pk

    res = client.patch(f'{endpoint}/bulk-notifications/{_id}', data={'message': 'Test update'})
    assert res.status_code == 200
    assert BulkNotification.objects.first().message == 'Test update'

    res = client.put(f'{endpoint}/bulk-notifications/{_id}', data=bulk_notification)
    assert res.status_code == 200
    assert BulkNotification.objects.first().message == bulk_notification['message']

    res = client.delete(f'{endpoint}/bulk-notifications/{_id}')
    assert res.status_code == 204
    assert BulkNotification.objects.count() == 0

