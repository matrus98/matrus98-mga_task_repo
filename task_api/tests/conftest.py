import pytest
import requests

from rest_framework import status


@pytest.fixture(scope='function')
def all_tasks():
    return requests.get('http://localhost:8000/api/').json()
