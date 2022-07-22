import logging
from flask import Flask
from flask_socketio import SocketIO

from app.config import config
from celery import Celery
from redis import Redis

import eventlet
eventlet.monkey_patch()

celery = Celery(__name__)
redis = Redis()
socketio = SocketIO()

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(env='development'):
    app = Flask(__name__)
    # setting logging
    handler = logging.FileHandler('logs/app.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    # loading config
    if env == "production":
        app.logger.info("載入 production")
        app.config.from_object(config[env])
    elif env == "development":
        app.logger.info("載入 development")
        app.config.from_object(config[env])
    else:
        logging.error("載入環境配置錯誤")
    # redis
    redis.from_url(url=f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}", charset='utf-8',
                   decode_responses=True)
    # celery
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    from app.tasks import setup_periodic_tasks
    # blueprint
    from app.views import simple_page

    app.register_blueprint(simple_page)

    from app.socket import MyCryptoPriceNamespace

    socketio.on_namespace(MyCryptoPriceNamespace('/ws'))
    # socket_io
    socketio.init_app(app, cors_allowed_origins='*', message_queue='redis://', async_mode='eventlet')
    return app
