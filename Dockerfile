FROM python:3.12.1-alpine3.19

LABEL author="Mateusz Ruszkowski"
LABEL version="1.0"

ENV PYTHONBUFFERED 1
ENV app_root=/mga
ENV app_dir=/mga_task
ENV is_docker_running_env_variable=True

COPY ./requirements.txt /requirements.txt
RUN pip install psycopg2-binary
RUN pip install -r /requirements.txt

RUN mkdir ${app_root}
RUN mkdir ${app_root}/${app_dir}
WORKDIR ${app_root}
COPY ./gunicorn.conf ${app_root}
COPY .${app_dir} ${app_root}/${app_dir}

RUN mkdir -p /tmp/gunicorn
RUN adduser -D guni_container_king
RUN chown guni_container_king.guni_container_king /tmp/gunicorn/ -R
#USER guni_container_king