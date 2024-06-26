[![Docker Image CI](https://github.com/matrus98/matrus98-mga_task_repo/actions/workflows/docker-image.yml/badge.svg)](https://github.com/matrus98/matrus98-mga_task_repo/actions/workflows/docker-image.yml)

# This project shows skills of usage the following technologies:
<ul>
    <li>Python</li>
    <li>Pytest</li>
    <li>Django</li>
    <li>Django REST framework</li>
    <li>Gunicorn</li>
    <li>Postgresql</li>
    <li>Docker</li>
    <li>Terraform</li>
</ul>
LinkedIn of author: https://www.linkedin.com/in/mateusz-ruszkowski/

Prerequirements:
    <ul>
        <li>Running docker engine</li>
    </ul>

It takes only few steps to launch application - which are:
<ol>
    <li>
        Choose empty folder, open here terminal and clone repository: <code>git clone https://github.com/matrus98/matrus98-mga_task_repo.git</code></li>
        In case lacking of git tool just download repository as zip file
    </li>
    <li>
        Next, run the following command (in directory where 'docker-compose.yml' file is present): <code>docker compose up</code>
        Make sure none of ports defined in file '.env' are in use.
    </li>
    <li>
        Log into container 'my_web_app'. At this point application will not work until migration is done.
        To achieve this run the following commands:
        <code>python manage.py makemigrations</code> and
        <code>python manage.py migrate</code>
        Database system is going to create 'postgres_data' folder in the same location as 'docker-compose.yml'. Since this folder exists there is no need to run these commands on next launch of cointainers.
    </li>
    <li>
        Actually that's it! Type in browser: <a href="http://localhost">localhost</a> and enjoy the application!
    </li>
</ol>

To test HTTP API Endpoints 'curl' tool might be used. Below are listed examples to test them. Watch the syntax. Author was using Windows operating system and got 'curl' tool <a href="https://curl.se/windows/">from this page</a>, opened PowerShell in directory where executable file was stored (of course it could be added to enviromental variable PATH):

* Create new task: <code>curl.exe -X POST -d 'name=TestCURL&description=I hope it is gonna work&author=Anonymous&status=Nowy&assigned_user=' http://localhost/api/task/ </code>

* Get all tasks: <code>curl.exe http://localhost/api/task/ </code>

* Get filtered tasks: <code>curl.exe http://localhost/api/task/?status=Nowy&assigned_user=&name_description=&</code>
Possible values for 'field_to_be_filtered' are: name_description (filter by phrase in name or description of task), status (filter by status), assigned_user (filter by user which is assigned to tasks)

* Get task details: <code>curl.exe http://localhost/api/task/<task_id> </code>

* Edit task data: <code>curl.exe -X PATCH -d 'description=New examples description&status=Rozwiązany' http://localhost/api/task/<task_id>/ </code>

* Delete task: <code>curl.exe -X DELETE http://localhost/api/task/<task_id>/ </code>

* Get events (what action took place and which task it applied to): <code>curl.exe http://localhost/api/history/ </code>

* Get events for particular task till certain date: <code>curl.exe 'http://localhost:8000/api/history/?historical_task_id=<task_id>&occurrence_date=<i>time</i>' </code>
This works event if task no longer exists in database (requires knowing what 'id' it had and we know that the 'id' is unique). Time can be promped in either format "2024-02-05T12:30:51.162912Z" or "2024-02-05T12:30". It refers to example date 5th February 2024 12:30. If no time is provided then all events are returned, and thus command <code>curl.exe 'http://localhost:8000/api/history/?historical_task_id=<task_id>&occurrence_date=<i>time</i>' </code> get every event related to given task up to current time.

Time can be promped in either format "2024-02-05T12:30:51.162912Z" or "2024-02-05T12:30". It refers to example date 5th February 2024 12:30.

To run tests run command <code>pytest</code> in root directoy of application. Below is attached screen which run tests only written for 'task_api' module.<br/><br/>
![Pytest screen](test_screen.png)
