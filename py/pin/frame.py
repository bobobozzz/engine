from functools import wraps
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache, select_autoescape, Template
import re
import sys
import json

if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def singleton(class_):
    instances = {}

    @wraps(class_)
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Pin:
    def __init__(self):
        self.map = {}

    def route(self, pattern, method=['POST']):
        def wrapper_a(func):
            if pattern not in self.map:
                self.map[pattern] = {'method': method, 'callback': func,'regex':re.compile(pattern)}

            @wraps(func)
            def wrapper_b(req, res, param):
                func(req, res, param)
            return wrapper_b
        return wrapper_a
        
    def run(self, req, res):
        for k, v in self.map.items():
            if req.method() in v['method']:
                m = v['regex'].match(req.uri())
                if m:
                    v['callback'](req, res, m.groupdict())
                    break

    def response_json(err_code, err_msg, data):
        res.header('Content-Type','text/plain;charset=utf-8')
        result = {"err_code": err_code,
                "err_msg": err_msg,
                "data": data}
        res.content(json.dumps(result))
        res.status(200)

@singleton
class View:
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
        self.jinja2_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            bytecode_cache=FileSystemBytecodeCache(self.templates_dir),
            auto_reload=False,
            optimized=True,
            autoescape=select_autoescape(['htm', 'html', 'xml', 'json']))

    def render(self, template_file, variable):
        engine = self.jinja2_env.get_template(template_file)
        result = engine.render(variable)
        return str(result)

    def str_render(self, template_string, variable):
        engine = Template(template_string)
        result = engine.render(variable)
        return str(result)

    def forward(res, result, tpl_name):
        res.header('Content-Type','text/plain;charset=utf-8')
        res.content(view.render(tpl_name, result))
        res.status(200)

