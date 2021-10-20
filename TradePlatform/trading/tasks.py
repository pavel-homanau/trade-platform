from TradePlatform.celery import app
from trading.services import CreateTrade


@app.task
def create_trade_task():
    CreateTrade.execute({})
