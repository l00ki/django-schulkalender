# Django-Schulkalender

Schulkalender als Django app.


Installation
-----------

1. F&uuml;ge "schulkalender" zu INSTALLED_APPS hinzu::

    INSTALLED_APPS = [
        ...
        'schulkalender',
    ]

2. Inkludiere die Schulkalender URLconf in urls.py::

    path('polls/', include('polls.urls')),

3. F&uuml;hre ``python manage.py migrate`` aus um die Schulkalender-Models zu erstellen.

4. Starte den Development Server und navigiere zu http://127.0.0.1:8000/kalender/
