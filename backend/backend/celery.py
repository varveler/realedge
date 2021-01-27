# coding=UTF8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery('backend')

#CELERY_TIMEZONE = 'UTC'

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

"""
app.conf.beat_schedule = {
    'save_user_weekly_metrics': {
        'task': 'save_user_weekly_metrics',
        'schedule': crontab(minute=40, hour=19, day_of_week='sat'),
    },
}
"""