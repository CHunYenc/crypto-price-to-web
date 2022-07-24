import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_socketio import SocketIO

from app.config import config
from celery import Celery
import eventlet

eventlet.monkey_patch()

celery = Celery(__name__)
socketio = SocketIO()


def make_celery(app):
    # redis
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)
    # setting logging
    log_file = os.path.join(os.getcwd(), *['logs', 'app.log'])
    handler = TimedRotatingFileHandler(filename=log_file, when='MIDNIGHT', interval=1)
    # handler = logging.FileHandler('logs/app.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    config_name = app.config["ENV"].lower()

    # loading config
    if config_name == "production":
        app.logger.info("載入 production")
        app.config.from_object(config[config_name])
    elif config_name == "development":
        app.logger.info("載入 development")
        app.config.from_object(config[config_name])
    else:
        logging.error("載入環境配置錯誤")
    # celery
    make_celery(app)
    with app.app_context():
        from app import tasks
        # blueprint
        from app.views import simple_page
        app.register_blueprint(simple_page)
        from app.socket import MyCryptoPriceNamespace
        socketio.on_namespace(MyCryptoPriceNamespace('/ws'))
        # socket_io
        socketio.init_app(app, cors_allowed_origins='*',
                          message_queue=f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}",
                          async_mode='eventlet', engineio_logger=True)
    return app
