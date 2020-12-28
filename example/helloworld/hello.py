#!/usr/bin/env python3

#BoBoBo#

from pin.router import engine_app


def wsgi_app(environ, start_response):
    params = environ['QUERY_STRING']
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello World!\n'.encode('utf-8'), ('QUERY_STRING:' + params).encode('utf-8')]


app = engine_app(wsgi_app)

if __name__ == "__main__":
    import pin.embed.server as server
    server.bootstrap(wsgi_app)
