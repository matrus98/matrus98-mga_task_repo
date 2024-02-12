import pytest
import requests
import datetime

from rest_framework import status


def test_get_filtered_event_history_list_for_task(all_tasks):
    json = {
        "historical_task_id": all_tasks[0]['id'],
        "task_name": "Does not exists",
        "user_who_edited": "MR. PYTEST",
        "assigned_user": "-----",
        "action": "Heh",
        "fields_to_update": ['description'],
        "old_values": ['old one'],
        "new_values": ['into new one'],
        "occurrence_date": None,
        "task": None
    }

    url = 'http://localhost:8000/api/history/'
    response = requests.post(url, json)
    assert response.status_code == status.HTTP_201_CREATED
