#!/usr/bin/env python3

#BoBoBo#

from datetime import date, datetime
import os
import sys
import json
import pin.kit.util as util
import pin.kit.common as common

from jinja2 import Environment, \
    FileSystemLoader, \
    FileSystemBytecodeCache, \
    select_autoescape, \
    Template


def tpl_path(conf=None):
    if not conf:
        conf = common.get_conf(None)
    path = conf('app', 'template_path', None)
    return path


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def response_json(result, headers=None):
    res = {}
    res['headers'] = []
    res['headers'].append(('Content-Type', 'application/json;charset=utf-8'))
    if headers:
        res['headers'] += list(map(lambda k: (k, headers[k]), headers))
    res['status'] = '200 OK'
    res['content'] = json.dumps(result, cls=ComplexEncoder)
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

    print('Use template path: ' + tpl_path)

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


def config_render(conf):
    global render
    render = view(tpl_path(conf))
