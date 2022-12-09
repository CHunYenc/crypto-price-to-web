# CRYPTO-SCHEDULER

# 使用方法

## 建立 backend/.env

```dosini
// .env
SECRET_KEY = b1bfe26f1e4e7c9433ada16e52a447ecc50d9e4ed4148126d0c3a6b3acf307c3
REDIS_HOST = redis
REDIS_PORT = 6379
```

> 你可以使用下面的方式產生 SECRET_KEY

```shell
$ python3 -c 'import secrets; print(secrets.token_hex())'
b1bfe26f1e4e7c9433ada16e52a447ecc50d9e4ed4148126d0c3a6b3acf307c3
```

# Error

## ImportError: cannot import name 'Celery' from 'celery'

```shell
$ pip install importlib-metadata-4.8.3
```

[reference](https://github.com/python/importlib_metadata/issues/411)