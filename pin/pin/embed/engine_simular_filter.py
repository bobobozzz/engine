#!/usr/bin/env python3

#BoBoBo#


import re


def auth_filter(headers, auth_header_name, token_storer):
    print('Headers after filter: ' + str(headers))
    new_headers = {}
    new_headers.update(headers)

    if not token_storer or not auth_header_name or '' == auth_header_name:
        return None

    if not auth_header_name in headers:
        auth_header_name = auth_header_name.lower()
        if not auth_header_name in headers:
            return None

    auth_token = headers[auth_header_name]
    if not auth_token or '' == auth_token:
        return None

    auth_str = token_storer.get_auth_str(auth_token)
    if not auth_str or '' == auth_str:
        return None

    del new_headers[auth_header_name]
    new_headers['Auth'] = auth_str
    return new_headers


def fit(rule, path):
    if not rule or '' == rule:
        return True

    if re.match(rule, path, flags=0):
        return True
    else:
        return False
