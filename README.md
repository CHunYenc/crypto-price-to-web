# crypto-price-scheduler

只是要讓 Google Sheet 透過 XML 的方式同步現在價格.

# 目錄
- [crypto-price-scheduler](#crypto-price-scheduler)
- [目錄](#目錄)
- [skills](#skills)
  - [Important Files](#important-files)
    - [How to create SECRET_KEY?](#how-to-create-secret_key)
    - [backend/config.py](#backendconfigpy)
    - [scheduler/config.py](#schedulerconfigpy)

# skills

finish skills: ```postgresql```、```flask```、```flask-apscheduler```

future skills: ```nginx```、```uwsgi```、```docker```、```docker-compose```

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


### backend/config.py

```
class Config:
    SECRET_KEY = "this is your secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class developmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:port/dbname"


class productionConfig(Config):
    DEBUG = False


config = {"dev": developmentConfig, "pro": productionConfig}

```

### scheduler/config.py

```
class Config:
    SECRET_KEY = "this is your secret_key"   
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class development(Config):
    SCHEDULER_API_ENABLED = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:port/dbname"


class production(Config):
    SCHEDULER_API_ENABLED = False
    DEBUG = False


config = {"dev": development, "pro": production}

```