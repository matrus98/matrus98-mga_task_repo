import pytest
import requests

from rest_framework import status


def test_add_task():
    url = 'http://localhost:8000/api/task/new'
    json = {
        "name": "PytestJSON",
        "description": "I hope it is gonna work",
        "user_who_edited": "Anonymous",
        "status": "Nowy",
        "assigned_user": None
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_by_name_description_list_of_tasks():
    url = 'http://localhost:8000/api/'
    json = {
        "phrase_string": "p",
        "field_to_be_filtered": "name_description"
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_by_status_list_of_tasks():
    url = 'http://localhost:8000/api/'
    json = {
        "phrase_string": "Nowy",
        "field_to_be_filtered": "status"
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_by_assigned_user_list_of_tasks():
    url = 'http://localhost:8000/api/'
    json = {
        "phrase_string": "p",
        "field_to_be_filtered": "assigned_user"
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK


def test_get_non_filtered_list_of_tasks():
    url = 'http://localhost:8000/api/'
    json = {
        "phrase_string": "Who cares now?",
        "field_to_be_filtered": "none"
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_bad_request_list_of_tasks():
    url = 'http://localhost:8000/api/'
    json = {
        "phrase_string": "Should be exception",
        "field_to_be_filtered": "filter which does not exists"
    }

    response = requests.post(url, json)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

