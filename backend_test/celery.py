from __future__ import absolute_import, unicode_literals
import os
from django.core.management import call_command
from celery import Celery
from celery.schedules import crontab
from subprocess import run

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_test.settings')

app = Celery('backend_test',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379',
             include=['backend_test.tasks'],
             timezone='America/Santiago',
             )

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='35', hour='9', day_of_week=[1, 2, 3, 4, 5]), update_rates.s())

@app.task
def update_rates():
    print('UPDATING RATES')
    #run(['django-admin', 'updaterates'])
    call_command('updaterates')

if __name__ == '__main__':
    app.start()