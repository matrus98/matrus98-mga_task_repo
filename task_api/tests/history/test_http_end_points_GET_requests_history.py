import pytest
import requests
import datetime

from rest_framework import status


def test_get_entire_history():
    url = 'http://localhost:8000/api/task/history'
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_rebuild_task_from_events(all_tasks):
    url = 'http://localhost:8000/api/task/history/{}/{}'.format(
        all_tasks[0]['id'],
        "{}T21:37:33.082339Z".format(datetime.date.today())
    )
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK
