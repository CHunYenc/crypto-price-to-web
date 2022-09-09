from calendar import c
import logging
from logging.config import dictConfig
from flask import Flask, render_template
from flask_socketio import SocketIO
from redis import Redis
from app.settings import config
import eventlet

eventlet.monkey_patch()
socketio = SocketIO()


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500


def make_celery(app, celery):
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def make_redis(app):
    redis = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    return redis


def create_app(env):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
            },
            'sameFile': {
                'format': '%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'flask': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                # TODO 'filename': os.path.join()
                'filename': 'logs/app.log',
                'formatter': 'default'
            },
            'celery': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'logs/celery.log',
                'formatter': 'sameFile'
            }
        },
        'loggers': {
            '': {
                'level': 'INFO',
                'handlers': ['flask', 'console']
            },
            'app.celery': {
                'handlers': ['celery', 'console'],
                'level': 'INFO',
                'propagate': False
            },
        }
    })

    app = Flask(__name__)
    app.config.from_object(config[env])
    app.logger.info(f"載入 {env}")

    with app.app_context():
        # celery
        from app.extensions import celery
        make_celery(app, celery)
        from app import tasks
        # blueprint
        from app.views import simple_page
        app.register_blueprint(simple_page)
        # error page handler
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(500, internal_server_error)
        # socket_io
        from app.socket import MyCryptoPriceNamespace
        socketio.on_namespace(MyCryptoPriceNamespace('/'))
        socketio.init_app(app, cors_allowed_origins='*',
                          message_queue=f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}",
                          async_mode='eventlet', engineio_logger=True
                          )
    return app
