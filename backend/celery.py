#  ==============================================================================================================================================================================================================================================================================================================================
#  File Name: celery.py
#  Description: This file serves the purpose of configuring and setting up the Celery distributed task queue system.

#  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================================================================================================================================================================================================================================================

from __future__ import absolute_import, unicode_literals

import os
#To implementation in celery with django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')