import pytest
import requests

from rest_framework import status


def test_get_all_tasks():
    url = 'http://localhost:8000/api/task/'

    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_get_detailed_task_exception_info():
    url = 'http://localhost:8000/api/task/0'

    response = requests.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_detailed_task_info(all_tasks):
    try:
        url = 'http://localhost:8000/api/task/{}'.format(all_tasks[0]['id'])
        response = requests.get(url)
        assert response.status_code == status.HTTP_200_OK
    except AttributeError:  # No tasks in database
        pass

