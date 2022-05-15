import logging

from flask import Flask
from app.config import config
from celery import Celery
from redis import Redis


def make_celery(app):
    celery = Celery(
        app.import_name
    )
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)

# setting logging
handler = logging.FileHandler('logs/app.log', encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

config_name = app.config["ENV"]

# loading config
if config_name == "production":
    app.logger.info("載入 production")
    app.config.from_object(config[config_name])
elif config_name == "development":
    app.logger.info("載入 development")
    app.config.from_object(config[config_name])
else:
    logging.error("載入環境配置錯誤")
# redis
redis = Redis.from_url(app.config["CACHE_REDIS_URL"])
# celery
celery = make_celery(app)
from app.tasks import setup_periodic_tasks
# blueprint
from app.views import simple_page

app.register_blueprint(simple_page)
# # db
# db.init_app(app)
# migrade.init_app(app, db)
