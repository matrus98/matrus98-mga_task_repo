import pytest
import requests
import datetime

from rest_framework import status


def test_get_filtered_event_history_list_for_task(all_tasks):
    json = {
        "id": all_tasks[0]['id'],
        "time": "{}T21:37:33.082339Z".format(datetime.date.today())
    }

    url = 'http://localhost:8000/api/task/history'
    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK
