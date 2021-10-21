from TradePlatform.celery import app
from trading.services import CreateTrade


@app.task
def create_trade_task():
    """Creates a trade."""
    CreateTrade.execute({})
