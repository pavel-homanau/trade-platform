import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradePlatform.settings')

app = Celery('TradePlatform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


if __name__ == '__main__':
    app.start()
