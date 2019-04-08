from gevent.local import local
from werkzeug.local import LocalProxy
from werkzeug.wrappers import Request
from contextlib import contextmanager

from gevent.pywsgi import WSGIServer

_requests = local()
request = LocalProxy(lambda: _requests.request)


@contextmanager
def sessionmanager(environ):
    _requests.request = Request(environ)
    yield
    _requests.request = None

def logic():
    response = "hello " + request.remote_addr
    return response.encode('utf-8')

def application(environ, start_response):
    status = '200 OK'
    with sessionmanager(environ):
        body = logic()
    # body=body.encode('utf-8')
    headers = [
        ('Content-Type', 'text/html')
    ]
    start_response(status, headers)
    return [body]


WSGIServer(('', 8000), application).serve_forever()
