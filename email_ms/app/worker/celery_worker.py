import os

from celery import Celery

celery_app = Celery(
    'celery',
    backend=os.environ.get("CELERY_BACKEND"),
    broker=os.environ.get("CELERY_BROKER")
)
celery_app.conf.imports = ('app.worker.task',)

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'send_email_task_ms': {
        'task': 'app.worker.task.send_email_task',
        'schedule': 20.0
    },
}
