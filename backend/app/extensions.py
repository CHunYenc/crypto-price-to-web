from redis import Redis


def make_redis(app):
    redis = Redis.from_url(url=F"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}")
    return redis
