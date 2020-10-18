#!/usr/bin/env python3

#BoBoBo#

def engine(request):
    body = request['body']
    response_body = 'Hello Engine! Receive:' + body
    return (response_body, len(response_body))
