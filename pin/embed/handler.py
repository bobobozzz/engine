#!/usr/bin/env python3

#BoBoBo#

from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import io
import json

from pin.controller import dispatch

class PinHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        datas = str(datas, 'utf-8')
        res = dispatch(self.path, datas)

        self.send_response(res['status'])
        for k, v in res['headers'].items():
            self.send_header(k, v)

        content = res['content']
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))
