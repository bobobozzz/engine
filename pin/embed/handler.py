#BoBoBo#

from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

class PinHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        self.pin_request = {}
        self.pin_request['request'] = self.request
        self.pin_request['headers'] = self.headers
        self.pin_request['method'] = self.command
        self.pin_request['uri'] = self.path

        self.pin_response = PinHTTPResponse()

        self.biz()
        self.send_response(self.pin_response.status)
        self.wfile.write(bytes(self.pin_response.content, 'utf-8'))

    def biz(self):
        pass

class PinHTTPResponse:

    def __init__(self):
        self.headers = {}

    def header(self, key, value):
        self.headers[key] = value

    def content(self, content):
        self.content = content

    def status(self, status):
        self.status = status
