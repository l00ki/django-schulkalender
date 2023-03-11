wsgi_app = "djangoinstance.wsgi:application"
loglevel = "debug"
workers = 1
bind = "0.0.0.0:8000"
reload = True
accesslog = errorlog = "dev.log"
capture_output = True
pidfile = "dev.pid"
daemon = False
