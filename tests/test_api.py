"""
Test the audio api CRUD operations
"""
import http.client
import random

from faker import Faker

fake = Faker()


def test_list_audio(client):
    audioType = ['song', 'podcast', 'audiobook']
    audioType = audioType[random.randint(0, 2)]

    response = client.get('/api/{}'.format(audioType))

    assert http.client.OK == response.status_code


def test_get_audio(client):
    audioType = ['song', 'podcast', 'audiobook']
    audioType = audioType[random.randint(0, 2)]

    newData = {
        'name': fake.name(),
        'title': fake.text()[:100],
        'host': fake.name(),
        'author': fake.name(),
        'narrator': fake.name(),
        'participants': [fake.name(), fake.name(), fake.name()],
        'duration': fake.pyint()
    }

    response = client.post('/api/{}'.format(audioType), json=newData)
    result = response.json

    assert http.client.OK == response.status_code

    response = client.get('/api/{}/{}'.format(audioType, result['ID']))
    assert http.client.OK == response.status_code


def test_create_audio(client):
    audioType = ['song', 'podcast', 'audiobook']
    audioType = audioType[random.randint(0, 2)]

    newData = {
        'name': fake.name(),
        'title': fake.text()[:100],
        'host': fake.name(),
        'author': fake.name(),
        'narrator': fake.name(),
        'participants': [fake.name(), fake.name(), fake.name()],
        'duration': fake.pyint()
    }

    response = client.post('/api/{}'.format(audioType), json=newData)

    assert http.client.OK == response.status_code


def test_update_audio(client):
    audioType = ['song', 'podcast', 'audiobook']
    audioType = audioType[random.randint(0, 2)]

    newData = {
        'name': fake.name(),
        'title': fake.text()[:100],
        'host': fake.name(),
        'author': fake.name(),
        'narrator': fake.name(),
        'participants': [fake.name(), fake.name(), fake.name()],
        'duration': fake.pyint()
    }

    response = client.post('/api/{}'.format(audioType), json=newData)
    result = response.json

    assert http.client.OK == response.status_code

    # update audio file

    updateData = {
        'name': fake.name(),
        'title': fake.text()[:100],
        'host': fake.name(),
        'author': fake.name(),
        'narrator': fake.name(),
        'participants': [fake.name(), fake.name(), fake.name()],
        'duration': fake.pyint()
    }

    response = client.put('/api/{}/{}'.format(audioType, result['ID']), json=updateData)
    assert http.client.OK == response.status_code


def test_delete_audio(client):
    audioType = ['song', 'podcast', 'audiobook']
    audioType = audioType[random.randint(0, 2)]

    newData = {
        'name': fake.name(),
        'title': fake.text()[:100],
        'host': fake.name(),
        'author': fake.name(),
        'narrator': fake.name(),
        'participants': [fake.name(), fake.name(), fake.name()],
        'duration': fake.pyint()
    }

    response = client.post('/api/{}'.format(audioType), json=newData)
    result = response.json

    assert http.client.OK == response.status_code

    response = client.delete('/api/{}/{}'.format(audioType, result['ID']))
    assert http.client.OK == response.status_code
