#FROM ubuntu:bionic
#RUN apt-get -y update \
#    && apt-get -y upgrade \
#    && apt-get install -y python3 \
#    && apt-get install -y python3-pip
    #&& apt-get install -y sqlite3 libsqlite3-dev
FROM python:3

ENV PYTHONUNBUFFERED 1

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir /opt/application
WORKDIR /opt/application

ENV FLASK_ENV=development
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV APPLICATION_DB=application
ENV POSTGRES_PORT=5432
ENV POSTGRES_HOSTNAME=localhost
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

ADD requirements /opt/requirements
#COPY requirements.txt requirements.txt
RUN pip install -r /opt/requirements/development.txt

#EXPOSE 5000
#COPY . .
