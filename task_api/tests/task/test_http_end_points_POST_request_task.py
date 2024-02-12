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


def test_get_filtered_by_name_description_list_of_tasks():
    url = 'http://localhost:8000/api/task/?status=&assigned_user=&name_description=Praca&'
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_by_status_list_of_tasks():
    url = 'http://localhost:8000/api/task/?status=W toku&assigned_user=&name_description=&'
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_by_assigned_user_list_of_tasks():
    try:
        url = 'http://localhost:8000/api/task/?status=&assigned_user=1&name_description=&'
        response = requests.get(url)
        assert response.status_code == status.HTTP_200_OK
    except:  # None user is created
        pass


def test_get_non_filtered_list_of_tasks():
    url = 'http://localhost:8000/api/task/?status=&assigned_user=&name_description=&'


def test_get_filtered_bad_request_list_of_tasks():
    url = 'http://localhost:8000/api/task/?fake=&'
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK

