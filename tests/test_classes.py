import requests

endpoint_url = 'http://10.151.209.38:5000/classes'


def test_index():
    response = requests.get(endpoint_url)
    assert response.status_code == 200


def test_add():
    payload = {"class_name": "pytest_str1",
               "class_short": "pytest_str2"}

    response = requests.post(endpoint_url, json=payload)
    assert response.status_code == 201

    response = requests.get(endpoint_url)
    data = response.json()
    assert data[-1]['class_name'] == payload['class_name']
    assert data[-1]['class_short'] == payload['class_short']


def test_delete():
    response = requests.get(endpoint_url)
    data = response.json()
    quantity = len(data)

    last_id = data[-1]['class_id']
    requests.delete(endpoint_url + f'/{last_id}')

    response = requests.get(endpoint_url)
    data = response.json()
    new_quantity = len(data)

    assert quantity == new_quantity + 1
