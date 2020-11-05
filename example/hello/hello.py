#!/usr/bin/env python3

#BoBoBo#

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    return ['Hello World!\n'.encode('utf-8')]

if __name__ == "__main__":
    import pin.embed.server as server
    server.bootstrap(app)
