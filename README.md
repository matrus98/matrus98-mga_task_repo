# This project shows skills of usage the following technologies:
<ul>
    <li>Python</li>
    <li>Django</li>
    <li>Django REST framework</li>
    <li>Gunicorn</li>
    <li>Postgresql</li>
    <li>Docker</li>
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
        Actually that's it! Type in browser: <a href="http://localhost:80">localhost</a> and enjoy the application!
    </li>
</ol>

To test HTTP API Endpoints 'curl' tool might be used. Below are listed examples to test them. Watch the syntax. Author was using Windows operating system and got 'curl' tool <a href="https://curl.se/windows/">from this page</a>, opened PowerShell in directory where executable file was stored (of course it could be added to enviromental variable PATH):
* Create new task: <code>curl.exe -X POST -d 'name=TestJSON&description=I hope it is gonna work&user_who_edited=Anonymous&status=Nowy&assigned_user=' http://localhost:8000/api/task/new </code>
* Get all tasks: <code>curl.exe http://localhost:8000/api/ </code>
* Get filtered tasks: <code>curl.exe -X POST -d 'phrase_string=p&field_to_be_filtered=name_description' http://localhost:8000/api/ </code>
* Get task details: <code>curl.exe http://localhost:8000/api/task/<task_id> </code>
* Edit task data: <code>curl.exe -X PATCH -d 'description=New examples description&status=Rozwiązany' http://localhost:8000/api/task/<task_id>/edit </code>
* Delete task: <code>curl.exe -X DELETE http://localhost:8000/api/task/<task_id>/delete </code>
* Get events (what action took place and which task it applied to): curl.exe http://localhost:8000/api/task/history
* Get events for particular task till certain date: </code>curl.exe -X POST -d 'id=<task_id>&time=<time>' http://localhost:8000/api/task/history </code>
This works event if task no longer exists in database (requires knowing what 'id' it had and we know that the 'id' is unique). Time can be promped in either format "2024-02-05T12:30:51.162912Z" or "2024-02-05T12:30". It refers to example date 5th February 2024 12:30. If no time is provided then all events are returned, and thus command <code>curl.exe -X POST -d 'id=<task_id>&time=<time>' http://localhost:8000/api/task/history </code> get every event related to given task up to current time
* Rebuild task to its state on given time: <code>curl.exe http://localhost:8000/api/task/history/<task_id>/<time> </code>
Time can be promped in either format "2024-02-05T12:30:51.162912Z" or "2024-02-05T12:30". It refers to example date 5th February 2024 12:30.
