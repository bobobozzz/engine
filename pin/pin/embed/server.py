#!/usr/bin/env python3

#BoBoBo#

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

def wrap_app(app):

    def wrapper(environ, start_response):
        setup_testing_defaults(environ)
        return app(environ, start_response)

    return wrapper

def bootstrap(app, host='', port=8080):
    app = wrap_app(app)
    with make_server(host, port, app) as httpd:
        print("Serving on port " + str(port) + " ...")
        httpd.serve_forever()
