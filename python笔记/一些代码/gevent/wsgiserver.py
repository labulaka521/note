from __future__ import print_function
from gevent.pywsgi import WSGIServer
import json

def application(env, start_response):
    print(env)
    if env['PATH_INFO'] == '/':
        start_response('200 OK',[('Content-type', 'text/html')])
        return [b'<b>hello in /</b>']
    elif env['PATH_INFO'] == '/api':
        start_response('200 OK', [('Content-type', 'text/html')])
        return [b'<b>hello in /api</b>']
    start_response('404 Not Found',[('Content-type','text/html')])
    return [b'<h1>Not Found</h1>']

if __name__ == '__main__':
    print('Serving on 8080')
    WSGIServer(('127.0.0.1', 8080), application).serve_forever()