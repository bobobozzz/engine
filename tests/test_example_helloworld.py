#!/usr/bin/env python3

#BoBoBo#

import requests


def test_get():
    resp = requests.get('http://localhost:8080/',
                        params={'p1': 'v1', 'p2': 'v2'})
    assert not resp.text is None
    lines = resp.text.split('\n')
    assert 'Hello World!' == lines[0]
    assert 'QUERY_STRING:p1=v1&p2=v2' == lines[1]
