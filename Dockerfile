FROM python:3

WORKDIR /code

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# app
COPY . /code/django-schulkalender
RUN ls
WORKDIR /code/django-schulkalender
RUN pip install .

# instance
WORKDIR /code
RUN django-admin startproject djangoinstance
WORKDIR /code/djangoinstance
COPY db.sqlite3 .
COPY resources/settings.py djangoinstance
COPY resources/urls.py djangoinstance

