from notifications.models import Client

endpoint = '/api/v1/notifications'


def test_e2e_bulk_client(client):
    notification_client = {
        'number': 123456789,
        'code': '+37529',
        'tag': 'test',
        'timezone': 'Europe/Luxembourg'
    }

    res = client.post(f'{endpoint}/clients', data=notification_client)
    assert res.status_code == 201
    assert Client.objects.count() == 1
    assert Client.objects.first().number == 123456789

    res = client.get(f'{endpoint}/clients')
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {**notification_client}

    _id = Client.objects.first().pk

    res = client.patch(f'{endpoint}/clients/{_id}', data={'number': 123123})
    assert res.status_code == 200
    assert Client.objects.first().number == 123123

    res = client.put(f'{endpoint}/clients/{_id}',
                     data=notification_client)
    assert res.status_code == 200
    assert Client.objects.first().number == notification_client['number']

    res = client.delete(f'{endpoint}/clients/{_id}')
    assert res.status_code == 204
    assert Client.objects.count() == 0


