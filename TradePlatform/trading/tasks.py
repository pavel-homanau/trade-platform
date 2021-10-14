from TradePlatform.celery import app
from datetime import datetime

from trading.models import Item


@app.task
def tst_task():
    print('task')


