#BoBoBo#

from http.server import BaseHTTPRequestHandler

class PinHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.do_POST()

    def do_POST(self):
        self.pin_request = {}
        self.pin_request['request'] = self.request
        self.pin_request['headers'] = self.headers
        self.pin_request['uri'] = self.path

        self.pin_response = {}

        self.biz()

    def biz(self):
        pass
