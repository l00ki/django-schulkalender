FROM python:3

WORKDIR /code


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
COPY resources/settings.py djangoinstance
COPY resources/urls.py djangoinstance

