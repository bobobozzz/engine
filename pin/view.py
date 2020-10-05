#!/usr/bin/env python3

#BoBoBo#

import os
import sys
import json
import configparser

from jinja2 import Environment, \
    FileSystemLoader, \
    FileSystemBytecodeCache, \
    select_autoescape, \
    Template

def tpl_path():
    conf = configparser.ConfigParser()
    conf_file = os.getcwd() + '/etc/app.conf' 
    conf.read(conf_file)
    path = conf.get('app', 'template_path')
    return path

def render_json(result, headers=None):
    res = {}
    res['headers'] = {}
    res['headers']['Content-Type'] = 'application/json;charset=utf-8'
    res['status'] = 200
    res['content'] = json.dumps(result)
    return res

def render_html(tpl_file, tpl_param={}, headers=None):
    res = {}
    res['headers'] = {}
    res['headers']['Content-Type'] = 'text/plain;charset=utf-8'
    res['status'] = 200
    res['content'] = render(tpl_file, tpl_param)
    return res

def render_404():
    res = {}
    res['headers'] = {}
    res['headers']['Content-Type'] = 'text/plain;charset=utf-8'
    res['status'] = 404
    return res

def response_json(err_code, err_msg, data):
    result = {"err_code": err_code,
            "err_msg": err_msg,
            "data": data}
    return result

def view(tpl_path):
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
