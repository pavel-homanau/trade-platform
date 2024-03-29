from TradePlatform.celery import app
from trading.services import CreateTrade, SendEmail


@app.task
def create_trade_task():
    CreateTrade.execute({})


@app.task
def create_send_email_task():
    SendEmail.execute({})
