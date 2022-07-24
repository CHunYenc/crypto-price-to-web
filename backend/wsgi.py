import eventlet
from eventlet import wsgi
from app import create_app

app = create_app()
wsgi.server(eventlet.listen(('', 8080)), app)
