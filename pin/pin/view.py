#!/usr/bin/env python3

#BoBoBo#

import os
import sys
import json
import pin.kit.util as util

from jinja2 import Environment, \
    FileSystemLoader, \
    FileSystemBytecodeCache, \
    select_autoescape, \
    Template


def tpl_path():
    path = util.get_conf('app', 'template_path', None)
    return path


def response_json(result, headers=None):
    res = {}
    res['headers'] = []
    res['headers'].append(('Content-Type', 'application/json;charset=utf-8'))
    if headers:
        res['headers'] += list(map(lambda k: (k, headers[k]), headers))
    res['status'] = '200 OK'
    res['content'] = json.dumps(result)
    return res


def response_html(tpl_file, tpl_param={}, headers=None):
    res = {}
    res['headers'] = []
    res['headers'].append(('Content-Type', 'text/html;charset=utf-8'))
    res['status'] = '200 OK'
    res['content'] = render(tpl_file, tpl_param)
    return res


def response_404():
    res = {}
    res['headers'] = []
    res['headers'].append(('Content-Type', 'text/html;charset=utf-8'))
    res['status'] = '404 Not Found'
    res['content'] = ''
    return res


def view(tpl_path):
    if not tpl_path:
        return None

    jinja2_env = Environment(
        loader=FileSystemLoader(tpl_path),
        bytecode_cache=FileSystemBytecodeCache(tpl_path),
        auto_reload=False,
        optimized=True,
        autoescape=select_autoescape(['htm', 'html', 'xml', 'json']))

    def render(tpl_file, variable):
        engine = jinja2_env.get_template(tpl_file)
        result = engine.render(variable)
        return str(result)

    return render


render = view(tpl_path())
