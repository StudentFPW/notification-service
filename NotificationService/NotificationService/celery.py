import os

from celery import Celery

# The line `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotificationService.settings')` is setting the value of the
# environment variable `DJANGO_SETTINGS_MODULE` to `'NotificationService.settings'` ↓.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotificationService.settings')

# The code `app = Celery('NotificationService')` creates a new instance of the Celery class with the name
# 'NotificationService'. This instance will be used to configure and run the Celery tasks ↓.
app = Celery('NotificationService')
app.config_from_object('django.conf:settings', namespace='CELERY')

# `app.autodiscover_tasks()` is a method provided by Celery that automatically discovers and registers task modules in
# your Django project ↓.
app.autodiscover_tasks()
