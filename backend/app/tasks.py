import json

from app.extensions import make_redis
from . import celery
from flask import current_app as app
import ccxt

r = make_redis(app)

@celery.task
def every_second_task():
    # print(datetime.now(), "task1")
    app.logger.info('running my task')


@celery.task
def get_binance_tickers():
    data = ccxt.binance().fetch_tickers()
    NAME = str.upper("crypto_binance")
    r.set(NAME, json.dumps(data))
    app.logger.info("get binance tickers")
    r.close()


@celery.task
def get_cryptocom_tickers():
    data = ccxt.cryptocom().fetch_tickers()
    NAME = str.upper("crypto_cryptocom")
    r.set(NAME, json.dumps(data))
    app.logger.info("get crypto tickers")
    r.close()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(1.0, every_second_task, name='add-every-1')
    sender.add_periodic_task(10.0, get_binance_tickers, name='get-binance-every-5')
    sender.add_periodic_task(10.0, get_cryptocom_tickers, name='get-cryptocom-every-5')
