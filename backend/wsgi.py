import eventlet
from eventlet import wsgi
from app import create_app

# app = create_app('development')
app = create_app('production')
wsgi.server(eventlet.listen(('', 8080)), app)
