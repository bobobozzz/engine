#!/usr/bin/env python3

#BoBoBo#

import json
import sys
from http import HTTPStatus
from functools import wraps
from traceback import format_exc
from io import BytesIO
import threading
import traceback
from urllib.parse import parse_qs
from html import escape

from pin.view import response_404
from pin.view import response_json
from pin.kit.util import html_escape
from pin.kit.common import errcode_ret


def router():
    url_map = {}

    def route(url, response_=response_json):
        def wrapper_a(func):
            def wrapper_b(*args, **kw):
                try:
                    return response_(func(*args, **kw))
                except Exception as e:
                    print('Error: %s' % traceback.format_exc())
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
        try:
            auth_param = environ['AUTH']
            if auth_param and '' != auth_param:
                auth_param = json.loads(auth_param)
        except Exception as e:
            print('Failed to parse auth data for: ' + str(e))
            auth_param = None

        if 'GET' == method:
            query = environ['QUERY_STRING']
            if '' == query:
                if auth_param:
                    return action(auth_param)
                else:
                    return action()
            else:
                querys = query.split('&')
                querys = list(map(lambda s: s.split('='), querys))
                querys_key = list(map(lambda s: s[0], querys))
                querys_value = list(map(lambda s: s[1], querys))
                param = dict(zip(querys_key, querys_value))
                if auth_param:
                    return action(auth_param, **param)
                else:
                    return action(**param)

        elif 'POST' == method:
            try:
                environ_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                environ_body_size = 0
            print("Server received content length: " + str(environ_body_size))
            environ_body = environ['wsgi.input'].read(environ_body_size)
            print("Server received content: " + str(environ_body))
            nd = environ_body.decode("utf8")
            print("Server received content escaped: " + nd)
            nd = json.loads(nd)
            if auth_param:
                return action(auth_param, **nd)
            else:
                return action(**nd)
        else:
            return action(environ)


def pin_app(debug):

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


def escape_dict(d):
    sd = {}
    for k in d.keys():
        sk = escape(k.decode("utf8"))
        if isinstance(d[k], dict):
            sd[sk] = escape_dict(d[k])
        elif isinstance(d[k], list):
            nl = []
            for i in range(len(d[k])):
                nl.append(escape_dict(d[k][i]))
            sd[sk] = nl
        else:
            v = escape(d[k].decode("utf8"))
            sd[sk] = v

    return sd
