from app import create_app

app = create_app('production')
app.app_context().push()

from app.extensions import celery

# celery -A celery_worker.celery worker -P eventlet -c 1000 --loglevel=info
# celery -A celery_worker.celery beat -l info
