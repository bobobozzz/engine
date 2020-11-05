#!/usr/bin/env python3

#BoBoBo#

import json
from http import HTTPStatus
from functools import wraps
from pin.view import response_404

def router():
    url_map={}

    def route(url, render):
        def wrapper_a(func):
            def wrapper_b(*args):
                return render(func(*args))

            url_map[url] = wrapper_b
            return wrapper_b
        return wrapper_a

    return url_map, route

urls, route = router()

def dispatch(request):
    path = request['PATH_INFO']
    action = urls.get(path)
    if None is action:
        return response_404()
    else:
        #TODO: check content-type and parse param
        method = request['REQUEST_METHOD']
        if 'GET' == method:
            query = request['QUERY_STRING']
            if '' == query:
                action(None)
            else:
                querys = query.split('&')
                querys = list(map(lambda s : s.split('='), querys))
                querys_key = list(map(lambda s:s[0], querys))
                querys_value = list(map(lambda s:s[1], querys))
                param = dict(zip(querys_key, querys_value))
                return action(param)
        else:
            return action(request)

def pin_app(debug=False):

    def app(environ, start_response):
        if debug:
            print(environ)
        try:
            response = dispatch(environ)
        except (KeyboardInterrupt, SystemExit, MemoryError):
                raise
        except Exception as E:
            err = '<h1>Critical error while processing request: %s</h1>' \
                  % html_escape(environ.get('PATH_INFO', '/'))
            if debug:
                err += '<h2>Error:</h2>\n<pre>\n%s\n</pre>\n' \
                       '<h2>Traceback:</h2>\n<pre>\n%s\n</pre>\n' \
                       % (html_escape(repr(E)), html_escape(format_exc()))
            headers = [('Content-Type', 'text/html; charset=UTF-8')]
            start_response('500 INTERNAL SERVER ERROR', headers, sys.exc_info())
            return [to_bytes(err)]
        else:
            start_response(response['status'], response['headers'])
            return [to_bytes(response['content'])]

    return app

def to_bytes(s, enc='utf8', err='strict'):
    return s.encode(enc)
