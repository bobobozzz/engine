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


class EngineHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.do_POST()

    def do_GET(self):
        content_length = self.headers['content-length']
        if None is content_length:
            datas = '{}'
        else:
            datas = self.rfile.read(int(content_length))
            datas = str(datas, 'utf-8')

        paths = self.path.split('?')
        request = {}
        request['PATH_INFO'] = paths[0]
        request['REQUEST_METHOD'] = 'GET'
        request['QUERY_STRING'] = paths[1]
        res = self.do_app(request)

        self.send_response(200)
        for h in res['headers']:
            self.send_header(h[0], h[1])

        content = bytes()
        for c in res['content']:
            content = content + c

        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

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

    #handler_class = partial(biz_handler_class, directory=args.directory)
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
