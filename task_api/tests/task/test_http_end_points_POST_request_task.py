import pytest
import requests

from rest_framework import status


def test_add_task():
    url = 'http://localhost:8000/api/task/'

    json = {
        'author': 'Anonymous',
        'name': 'PytestJSON',
        'description': 'I hope it is gonna work',
        'assigned_user': None,
        'status': 'Nowy',
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_201_CREATED

