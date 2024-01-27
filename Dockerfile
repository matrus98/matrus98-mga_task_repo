FROM python:3.12.1-alpine3.19

LABEL author="Mateusz Ruszkowski"
LABEL version="1.0"

ENV PYTHONBUFFERED 1
ENV app_root=/mga
ENV is_docker_running_env_variable=True

RUN mkdir ${app_root}
WORKDIR ${app_root}
COPY . .
RUN pip install psycopg2-binary
RUN pip install -r ./requirements.txt

RUN mkdir -p /tmp/gunicorn
RUN adduser -D guni_container_king
RUN chown guni_container_king.guni_container_king /tmp/gunicorn/ -R
RUN chown guni_container_king.guni_container_king ${app_root} -R
USER guni_container_king