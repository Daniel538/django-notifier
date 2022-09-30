from notifications.models import Client

endpoint = '/api/v1/notifications'


def test_e2e_bulk_client(api_client):
    notification_client = {
        'number': 123456789,
        'code': '+37529',
        'tag': 'test',
        'timezone': 'Europe/Luxembourg'
    }

    res = api_client.post(f'{endpoint}/clients', data=notification_client)
    assert res.status_code == 201
    assert Client.objects.count() == 1
    assert Client.objects.first().number == 123456789

    res = api_client.get(f'{endpoint}/clients')
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == {**notification_client}

    _id = Client.objects.first().pk

    res = api_client.patch(f'{endpoint}/clients/{_id}', data={'number': 123123})
    assert res.status_code == 200
    assert Client.objects.first().number == 123123

    res = api_client.put(f'{endpoint}/clients/{_id}',
                         data=notification_client)
    assert res.status_code == 200
    assert Client.objects.first().number == notification_client['number']

    res = api_client.delete(f'{endpoint}/clients/{_id}')
    assert res.status_code == 204
    assert Client.objects.count() == 0
