from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mazeratsite.settings")
# django.setup()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mazeratsite.settings')

app = Celery('mazeratsite')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# python -m celery -A mazeratsite beat --loglevel=debug
# python -m celery -b redis://127.0.0.1:6379/0 status
# python -m celery -A mazeratsite worker --loglevel=info
# python -m celery -A mazeratsite worker --pool=solo --loglevel=info

