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
<ol>
