# CRYPTO-SCHEDULER

# 使用方法

內容主要是 backend 要使用的環境變數。

```docker-compose``` 會使用 ```.env``` 的參數建立環境變數。

```
# .env
SECRET_KEY = ?? # required (必要)
- 
HOST = ?? # default 0.0.0.0
PORT = ?? # default 8080
REDIS_URL = ?? # default redis://localhost:6379
```

# Error

## ImportError: cannot import name 'Celery' from 'celery'

```shell
$ pip install importlib-metadata-4.8.3
```

[reference](https://github.com/python/importlib_metadata/issues/411)