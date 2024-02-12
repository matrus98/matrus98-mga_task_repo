import copy
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task, HistoricalTaskEvent
from .froms import TaskForm, FilterTaskForm, FilterHistoryForm
from .filters import TaskFilter, HistoricalTaskEventFilter
from os import environ as envs
from os.path import join

forbidden_list = ['_state', '_django_version', 'id']
map_value = 'assigned_user_id'
ROOT_ENDPOINT = 'http://localhost:{}/api/' \
                    .format(envs['MY_WEB_APP_EXTERNAL_PORT'] if 'is_docker_running_env_variable' in envs else '8000')


def _create_event(response, old_values, current_user, assigned_user_name, action_type):
    response_list = list(response)
    event_json = {
        "historical_task_id": response['id'],
        "task_name": response['name'],
        "user_who_edited": current_user,
        "assigned_user": assigned_user_name,
        "action": action_type,
        "fields_to_update": response_list,
        "old_values": [item for item in old_values],
        "new_values": [response[key] for key in response_list],
        "occurrence_date": timezone.now(),
        "task": response['id']
    }
    return requests.post(ROOT_ENDPOINT + 'history/', event_json)


def task_list(request):
    tasks = None

    if request.method == 'POST':
        filter_task_form = FilterTaskForm(request.POST)
        if filter_task_form.is_valid():
            form_parameters = filter_task_form.cleaned_data
            end_point = ROOT_ENDPOINT + 'task/?'
            for key in form_parameters:
                end_point += f'{key}={form_parameters[key]}&'

            tasks = requests.get(end_point).json()
            if type(tasks) != list:
                tasks = []
    else:
        tasks = requests.get(ROOT_ENDPOINT + 'task/').json()
        filter_task_form = FilterTaskForm()

    return render(request, 'task_list.html', {'tasks': tasks[::-1], 'form': filter_task_form})


def task_create_new(request):
    if request.method == 'POST':
        task_creation_form = TaskForm(request.POST)

        if task_creation_form.is_valid():
            end_point = ROOT_ENDPOINT + 'task/'
            task_msg = task_creation_form.cleaned_data
            assigned_user_name = '---'
            if task_msg['assigned_user'] != None:
                assigned_user_name = task_msg['assigned_user'].username
                task_msg['assigned_user'] = task_msg['assigned_user'].id
            current_user = request.user.username if request.user.username != '' else 'Anonymous'
            task_msg['author'] = current_user

            response = requests.post(end_point, task_msg).json()
            if str(response['assigned_user']).isdigit():
                response['assigned_user'] = assigned_user_name

            # Create event
            _create_event(
                response=response,
                old_values=['---' for i in range(len(list(response)))],
                current_user=current_user,
                assigned_user_name=assigned_user_name,
                action_type="Edit request"
            )

            return redirect('task_list')
    else:
        task_creation_form = TaskForm()

    return render(request, 'task_edit.html', {'form': task_creation_form})


def task_details(request, pk):
    task = requests.get(ROOT_ENDPOINT + f'task/{pk}').json()
    return render(request, 'task_details.html', {'task': task})


def task_edit(request, pk):
    task_json = requests.get(ROOT_ENDPOINT + f'task/{pk}').json()
    if request.method == "POST":
        task_edit_form = TaskForm(request.POST)

        if task_edit_form.is_valid():
            end_point = ROOT_ENDPOINT + 'task/{}/'.format(task_json['id'])
            task_msg = task_edit_form.cleaned_data
            assigned_user_name = '---'
            if task_msg['assigned_user'] != None:
                assigned_user_name = task_msg['assigned_user'].username
                task_msg['assigned_user'] = task_msg['assigned_user'].id
            current_user = request.user.username if request.user.username != '' else 'Anonymous'

            response = requests.patch(end_point, task_msg).json()
            if str(response['assigned_user']).isdigit():
                response['assigned_user'] = assigned_user_name

            # Create event
            _create_event(
                response=response,
                old_values=['---' for i in range(len(list(response)))],  # Is it here necessary?
                current_user=current_user,
                assigned_user_name=assigned_user_name,
                action_type="Edit request"
            )

            return redirect('task_details', pk=task_json['id'])
    else:
        task_edit_form = TaskForm()
        for key in task_json:
            if key in task_edit_form.fields:
                task_edit_form.fields[key].initial = task_json[key]

    return render(request, 'task_edit.html', {'form': task_edit_form})


def task_delete(request, pk):
    current_user = request.user.username if request.user.username != '' else 'Anonymous'
    response = {
        'id': pk,
        'name': 'TASK NO LONGER EXISTS'
    }
    # Create event
    _create_event(
        response=response,
        old_values=['---' for i in range(len(list(response)))],  # Is it here necessary?
        current_user=current_user,
        assigned_user_name='---',
        action_type='Delete request'
    )

    requests.delete(ROOT_ENDPOINT + f'task/{pk}')
    return redirect('task_list')


def task_history(request):
    end_point = ROOT_ENDPOINT + 'history/'
    task_events = False
    display_detailed_history_url_button = False
    the_one_task = None
    timezone_from_datetimefield = None

    if request.method == 'POST':
        task_events_form = FilterHistoryForm(request.POST)
        if task_events_form.is_valid():
            timezone_from_datetimefield = str(task_events_form.cleaned_data['occurrence_date'])

            if task_events_form.cleaned_data['historical_task_id'] == '' or task_events_form.cleaned_data['occurrence_date'] == None:
                timezone_from_datetimefield = str(timezone.now())
            if timezone_from_datetimefield.count(':') > 1:
                timezone_from_datetimefield = timezone_from_datetimefield[:timezone_from_datetimefield.find(':', timezone_from_datetimefield.find(':')+1)]
            timezone_from_datetimefield = timezone_from_datetimefield.replace(' ', 'T')

            end_point += '?historical_task_id={}&occurrence_date={}&'.format(
                task_events_form.cleaned_data['historical_task_id'],
                timezone_from_datetimefield
            )
            task_events = requests.get(end_point).json()[::-1]

            if task_events_form.cleaned_data['historical_task_id'] != '':
                display_detailed_history_url_button = True
                the_one_task = {
                    'id': task_events[0]['historical_task_id']
                }
                # for event in task_events:
                #     for field, new_value in zip(event.fields_to_update, event.new_values):
                #         if field == 'id':
                #             the_one_task['id'] = event['historical_task_id']
                #         else:
                #             the_one_task[field] = new_value

    else:
        task_events = requests.get(end_point).json()[::-1]
        task_events_form = FilterHistoryForm()

    return render(request, 'task_history.html', {'events': task_events,
                                                 'form': task_events_form,
                                                 'display_detailed_url': display_detailed_history_url_button,
                                                 'task': the_one_task,
                                                 'state_date': timezone_from_datetimefield})


def task_history_details(request, pk, time):
    end_point = ROOT_ENDPOINT + f'history/?historical_task_id={pk}&occurrence_date={time}&'
    archival_task = Task()
    events_related_to_task_before_the_set_time = requests.get(end_point).json()

    for event in events_related_to_task_before_the_set_time:
        if event['fields_to_update'] != None or event['new_values'] != None:
            for field, new_value in zip(event['fields_to_update'], event['new_values']):
                archival_task.__dict__[field] = new_value

    return render(request, 'task_history_details.html',
                  {'archival_task': archival_task, 'time': time})
