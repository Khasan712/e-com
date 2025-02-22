from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'task name': {
#         'task': 'task function path /v1/product/tasks/api_tasks | admin_tasks/foo_task',
#         'schedule': crontab(hour='*/24'), # terms
#     },
# }