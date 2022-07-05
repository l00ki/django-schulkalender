# Django-Schulkalender

Schulkalender Django app.

Installation
-----------

1. Installiere die app: ```pip3 install django-schulkalender-*.*.tar.gz```

2. F&uuml;ge "schulkalender" zu INSTALLED_APPS in ```settings.py``` der Django Website hinzu:

    INSTALLED_APPS = [
        ...
        'schulkalender',
    ]

3. Importiere die Schulkalender URLconf in urls.py::

    path('kalender/', include('schulkalender.urls')),

4. F&uuml;hre ```python manage.py migrate``` aus um die Schulkalender-Models zu erstellen.

5. Starte den Development Server und navigiere zu http://127.0.0.1:8000/kalender/
