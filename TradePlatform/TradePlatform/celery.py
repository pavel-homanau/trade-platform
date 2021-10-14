import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradePlatform.settings')

app = Celery('TradePlatform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "tst_task": {
        "task": "trading.tasks.tst_task",
        "schedule": 30.0
    }
}
