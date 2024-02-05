import pytest
import requests

from rest_framework import status


def test_update_first_task(all_tasks):
    json = {
        "description": "Test update string"
    }

    try:
        url = 'http://localhost:8000/api/task/{}/edit'.format(all_tasks[0]['id'])
        response = requests.patch(url, json)
        assert response.status_code == status.HTTP_200_OK
    except AttributeError:  # No tasks in database
        pass
