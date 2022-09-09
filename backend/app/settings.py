import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')


class developmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'


class productionConfig(Config):
    load_dotenv()
    ENV = 'production'
    DEBUG = False
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'


class testConfig(Config):
    ENV = 'test'
    TESTING = True
    REDIS_HOST = None
    REDIS_PORT = 6379
    CELERY_BROKER_URL = None
    CELERY_RESULT_BACKEND = None


config = {
    "development": developmentConfig,
    "production": productionConfig,
    "test": testConfig
}
