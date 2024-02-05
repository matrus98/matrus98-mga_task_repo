import copy

from rest_framework.response import Response
from rest_framework.decorators import api_view
from task_manager.models import Task, HistoricalTaskEvent
from .serializers import TaskSerializer, HistoricalTaskEventSerializer
from django.utils import timezone

forbidden_list = ['_state', '_django_version', 'id']
map_value = 'assigned_user_id'


@api_view(['GET', 'POST'])
def task_list(request):
    tasks = None
    if request.method == 'GET':
        tasks = Task.objects.all()

    elif request.method == 'POST':
        phrase_string = request.data.get('phrase_string')
        chosen_field_for_filtering = request.data.get('field_to_be_filtered')
        if chosen_field_for_filtering == 'name_description':
            tasks = (Task.objects.filter(name__icontains=phrase_string) |
                     Task.objects.filter(description__icontains=phrase_string))[::-1]
        elif chosen_field_for_filtering == 'status':
            tasks = Task.objects.filter(status__icontains=phrase_string)[::-1]
        elif chosen_field_for_filtering == 'assigned_user':
            tasks = Task.objects.filter(assigned_user__username__icontains=phrase_string)[::-1]

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def task_create_new(request):
    task = Task.objects.create(
        name=request.data.get('name'),
        description=request.data.get('description'),
        status=request.data.get('status'),
        assigned_user=request.data.get('assigned_user')
    )

    user_who_edited = request.data.get('user_who_edited') if 'user_who_edited' in request.data else ('HTTP API '
                                                                                                     'Endpoint has '
                                                                                                     'been used')
    event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
                                               user_who_edited=user_who_edited)
    event.action = 'Create (API)'
    assigned_user = task.assigned_user.username if task.assigned_user is not None else '---'
    event.assigned_user = assigned_user

    fields = set([atr for atr, value in task.__dict__.items() if atr not in forbidden_list])
    fields_to_update, old_values, new_values = [], [], []
    if map_value in fields:
        fields.remove(map_value)
        fields_to_update.append('assigned user')
        old_values.append('---')
        new_values.append(assigned_user)

    for atr in fields:
        fields_to_update.append(atr)
        old_values.append('---')
        new_values.append(task.__dict__[atr])
    event.fields_to_update = fields_to_update
    event.old_values = old_values
    event.new_values = new_values

    event.save()
    return Response()


@api_view(['GET'])
def task_details(request, pk):
    task = Task.objects.get(pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['PATCH'])
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    task_old = copy.copy(task)

    for key in request.data:
        if key in task.__dict__:
            task.__dict__[key] = request.data.get(key)

    task.save()

    user_who_edited = request.data.get('user_who_edited') if 'user_who_edited' in request.data else ('HTTP API '
                                                                                                     'Endpoint has '
                                                                                                     'been used')
    event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
                                               user_who_edited=user_who_edited)

    event.action = 'Update (API)'
    assigned_user = task.assigned_user.username if task.assigned_user is not None else '---'
    event.assigned_user = assigned_user

    fields_where_change_occurred = set([atr for atr, value in
                                        task_old.__dict__.items() ^ task.__dict__.items()
                                        if atr not in forbidden_list])

    fields_to_update, old_values, new_values = [], [], []
    if map_value in fields_where_change_occurred:
        fields_where_change_occurred.remove(map_value)
        fields_to_update.append('assigned user')
        old_values.append(task_old.assigned_user.username if task_old.assigned_user is not None else '---')
        new_values.append(assigned_user)

    for atr in fields_where_change_occurred:
        fields_to_update.append(atr)
        old_values.append(task_old.__dict__[atr])
        new_values.append(task.__dict__[atr])
    event.fields_to_update = fields_to_update
    event.old_values = old_values
    event.new_values = new_values

    event.save()

    return Response()


@api_view(['DELETE'])
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    user_who_edited = request.data.get('user_who_edited') if 'user_who_edited' in request.data else ('HTTP API '
                                                                                                     'Endpoint has '
                                                                                                     'been used')
    event = HistoricalTaskEvent.objects.create(task_id=task.id, task_name=task.name,
                                               user_who_edited=user_who_edited)
    event.action = 'Delete (API)'
    assigned_user = task.assigned_user.username if task.assigned_user is not None else '---'
    event.assigned_user = assigned_user

    fields = set([atr for atr, value in task.__dict__.items() if atr not in forbidden_list])
    fields_to_update, old_values, new_values = [], [], []
    if map_value in fields:
        fields.remove(map_value)
        fields_to_update.append('assigned user')
        old_values.append(assigned_user)
        new_values.append('---')

    for atr in fields:
        fields_to_update.append(atr)
        old_values.append(task.__dict__[atr])
        new_values.append('---')
    event.fields_to_update = fields_to_update
    event.old_values = old_values
    event.new_values = new_values

    task.delete()
    event.save()

    return Response()


@api_view(['GET', 'POST'])
def task_history(request):
    task_events = None
    if request.method == 'GET':
        task_events = HistoricalTaskEvent.objects.all().order_by('-occurrence_date')

    elif request.method == 'POST':
        task_state_till_date = request.data.get('time') if 'time' in request.data else timezone.now()
        task_state_till_date = task_state_till_date[:task_state_till_date.find(':', task_state_till_date.find(':')+1)]
        timezone_from_datetimefield = timezone.make_aware(
            timezone.datetime.strptime(task_state_till_date, '%Y-%m-%dT%H:%M'),
            timezone.get_default_timezone()
        )

        task_events = (HistoricalTaskEvent.objects
                       .filter(task_id=request.data.get('id'))
                       .filter(occurrence_date__lte=timezone_from_datetimefield)
                       .order_by('occurrence_date'))

    serializer = HistoricalTaskEventSerializer(task_events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_history_details(request, pk, time):
    archival_task = Task()

    task_state_till_date = time[:time.find(':', time.find(':') + 1)]
    timezone_from_datetimefield = timezone.make_aware(
        timezone.datetime.strptime(task_state_till_date, '%Y-%m-%dT%H:%M'),
        timezone.get_default_timezone()
    )

    events_related_to_task_before_the_set_time = (HistoricalTaskEvent.objects
                                                  .filter(task_id=pk)
                                                  .filter(occurrence_date__lte=timezone_from_datetimefield)
                                                  .order_by('occurrence_date'))

    for event in events_related_to_task_before_the_set_time:
        if event.fields_to_update is not None or event.new_values is not None:
            for field, new_value in zip(event.fields_to_update, event.new_values):
                archival_task.__dict__[field] = new_value

    serializer = TaskSerializer(archival_task)
    return Response(serializer.data)
