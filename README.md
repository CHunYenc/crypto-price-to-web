# crypto-price-scheduler

只是要讓 Google Sheet 透過 XML 的方式同步現在價格.

# 目錄
- [crypto-price-scheduler](#crypto-price-scheduler)
- [目錄](#目錄)
- [skills](#skills)
  - [Important Files](#important-files)
    - [How to create SECRET_KEY?](#how-to-create-secret_key)
    - [backend/config.py and scheduler/config.py](#backendconfigpy-and-schedulerconfigpy)

# skills

- Docker (Use Docker Services)
  - Docker-Compose
  - Redis
  - PostgreSQL
  - Nginx
- Flask (backend)
- Flask jinja2 (backend's html)
- Flask-apscheduler (scheduler)
- Uwsgi

## Important Files

### How to create SECRET_KEY?

```
==== generate SECRET_KEY ====
$ flask shell
>>> import os
>>> import base64
>>> a = os.urandom(24)
>>> base64.b64encode(a)
```


### backend/config.py and scheduler/config.py

```
class Config:
    SECRET_KEY = "this is your secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class developmentConfig(Config):
    SCHEDULER_API_ENABLED = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isyourpassword@host:port/postgres"
    CACHE_REDIS_URL = "redis://localhost:6379"



class productionConfig(Config):
    SCHEDULER_API_ENABLED = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:isyourpassword@host:port/postgres"
    CACHE_REDIS_URL = "redis://redis"


config = {"dev": developmentConfig, "pro": productionConfig}
```