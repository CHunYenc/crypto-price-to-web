import json
import logging

import ccxt
from app.extensions import celery
from app import make_redis
from flask import current_app as app

logger = logging.getLogger('app.celery')

redis = make_redis(app)


@celery.task
def every_second_task():
    logger.info('running my task')


@celery.task
def get_binance_tickers():
    data = ccxt.binance().fetch_tickers()
    NAME = str.upper("crypto_binance")
    redis.set(NAME, json.dumps(data))
    logger.info("get binance tickers")
    redis.close()


@celery.task
def get_cryptocom_tickers():
    data = ccxt.cryptocom().fetch_tickers()
    NAME = str.upper("crypto_cryptocom")
    redis.set(NAME, json.dumps(data))
    logger.info("get crypto tickers")
    redis.close()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(1.0, every_second_task, name='add-every-1')
    sender.add_periodic_task(10.0, get_binance_tickers, name='get-binance-every-5')
    sender.add_periodic_task(10.0, get_cryptocom_tickers, name='get-cryptocom-every-5')
