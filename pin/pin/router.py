#!/usr/bin/env python3

#BoBoBo#

import json
import sys
from http import HTTPStatus
from functools import wraps
from traceback import format_exc
from io import BytesIO
import threading

from pin.view import response_404
from pin.view import response_json
from pin.kit.util import html_escape
from pin.kit.util import errcode_ret
from pin.kit.util import logger


def router():
    url_map = {}

    def route(url, response_):
        def wrapper_a(func):
            def wrapper_b(**args):
                try:
                    return response_(func(**args))
                except Exception as e:
                    logger.exception(sys.exc_info())
                    return response_json(errcode_ret(-500, str(e), None))

            url_map[url] = wrapper_b
            return wrapper_b
        return wrapper_a

    return url_map, route


urls, route = router()


def dispatch(environ):
    path = environ['PATH_INFO']
    action = urls.get(path)
    if None is action:
        return response_404()
    else:
        method = environ['REQUEST_METHOD']
        if 'GET' == method:
            query = environ['QUERY_STRING']
            if '' == query:
                return action()
            else:
                querys = query.split('&')
                querys = list(map(lambda s: s.split('='), querys))
                querys_key = list(map(lambda s: s[0], querys))
                querys_value = list(map(lambda s: s[1], querys))
                param = dict(zip(querys_key, querys_value))
                return action(**param)
        elif 'POST' == method:
            try:
                environ_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                environ_body_size = 0
            environ_body = environ['wsgi.input'].read(environ_body_size)
            # d = cgi.parse(environ_body)
            return action(environ_body)
        else:
            return action(environ)


def pin_app(debug=False):

    def app(environ, start_response):
        nonlocal debug
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
            start_response('500 INTERNAL SERVER ERROR',
                           headers, sys.exc_info())
            return [to_bytes(err)]
        else:
            if debug:
                print(response)
            start_response(response['status'], response['headers'])
            return [to_bytes(response['content'])]

    return app


def engine_app(wsgi_app):

    def app(environ):
        local = threading.local()

        def start_response(status, headers):
            nonlocal local
            if None is headers:
                headers = []
            local.http_response_status = status
            local.http_response_headers = headers

        nonlocal wsgi_app
        res = wsgi_app(environ, start_response)
        response = {}
        response['headers'] = local.http_response_headers
        response['content'] = ''.join([from_bytes(b) for b in res])
        return response

    return app


def from_bytes(b, dec='utf8', err='strict'):
    return b.decode(dec)


def to_bytes(s, enc='utf8', err='strict'):
    return s.encode(enc)
