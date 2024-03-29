import pytest
import requests

from rest_framework import status


def test_delete_first_task(all_tasks):
    try:
        url = 'http://localhost:8000/api/task/{}/'.format(all_tasks[0]['id'])
        response = requests.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
    except AttributeError:  # No tasks in database
        pass
