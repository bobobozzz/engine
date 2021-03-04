#!/usr/bin/env python3

#BoBoBo#


import os
import contextlib
import socket
from http.server import *
from functools import partial
import sys
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import io
import json
import shutil
import pin.embed.engine_simular_filter as engine_simular_filter
from pin.kit.common import get_conf
import importlib


class EngineHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory

        self.filters = {}
        conf = get_conf('engine')
        auth_filter_rule = conf('filter', 'auth_filter_rule')
        self.filters['auth_filter_rule'] = auth_filter_rule
        self.auth_header_name = conf('filter', 'auth_header_name')
        try:
            self.token_storer = importlib.import_module(
                conf('filter', 'token_storer'))
        except Exception as e:
            print('Failed to get token storer for: ' + str(e))

        super().__init__(*args, **kwargs)

    def forbidden(self):
        self.response(403, None, json.dumps(
            {'errCode': 403, 'errMsg': 'Failed pass auth filter.'}))

    def response(self, code, headers, content):
        self.send_response(code)
        if headers:
            for h in headers:
                self.send_header(h[0], h[1])

        content = content.encode('utf8')
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

    def call_app(self, request):
        res = self.do_app(request)
        self.response(200, res['headers'], res['content'])

    def incoming_filter(self):
        path = self.path.split('?')[0]
        if engine_simular_filter.fit(self.filters['auth_filter_rule'], path):
            headers = engine_simular_filter.auth_filter(
                self.headers, self.auth_header_name, self.token_storer)
            if not headers:
                return False
            else:
                self.headers = headers
                return True

        return True

    def engine_request(self, method):
        paths = self.path.split('?')
        request = {}
        request['PATH_INFO'] = paths[0]
        request['AUTH'] = self.headers.get('Auth', None)
        request['REQUEST_METHOD'] = method
        request['CONTENT_LENGTH'] = self.headers.get('Content-Length', 0)
        request['CONTENT_TYPE'] = self.headers.get(
            'Content-Type', 'application/json')
        request['wsgi.input'] = self.rfile
        if len(paths) > 1:
            request['QUERY_STRING'] = paths[1]
        return request

    def do_POST(self):
        if not self.incoming_filter():
            return self.forbidden()
        request = self.engine_request('POST')
        self.call_app(request)

    def do_GET(self):
        if not self.incoming_filter():
            return self.forbidden()
        request = self.engine_request('GET')
        self.call_app(request)

    def do_app(self, request):
        print('Receive request: ' + str(requests))
        info = 'Need to be overrided by Subclass.'
        print(info)
        res = {}
        res['headers'] = {}
        res['content'] = info
        return res


def bootstrap(biz_handler_class=EngineHandler):
    args = server_args()

    # handler_class = partial(biz_handler_class, directory=args.directory)
    handler_class = biz_handler_class

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    serve(HandlerClass=handler_class,
          ServerClass=DualStackServer,
          port=args.port,
          bind=args.bind)


def serve(HandlerClass=BaseHTTPRequestHandler,
          ServerClass=ThreadingHTTPServer,
          protocol="HTTP/1.1", port=8080, bind=None):
    ServerClass.address_family, addr = _get_best_family(bind, port)

    HandlerClass.protocol_version = protocol
    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


def server_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    return args


def _get_best_family(*address):
    infos = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, type, proto, canonname, sockaddr = next(iter(infos))
    return family, sockaddr
