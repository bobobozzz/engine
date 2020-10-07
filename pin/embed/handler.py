#!/usr/bin/env python3

#BoBoBo#

from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import io
import json
import shutil

from pin.controller import dispatch

class PinHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        content_length = self.headers['content-length']
        if None is content_length:
            datas = '{}'
        else:
            datas = self.rfile.read(int(content_length))
            datas = str(datas, 'utf-8')

        request = {}
        request['path'] = self.path
        request['body'] = datas
        res = dispatch(request)

        self.send_response(res['status'])
        for k, v in res['headers'].items():
            self.send_header(k, v)

        content = res['content']
        content = content.encode('utf-8')          
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
