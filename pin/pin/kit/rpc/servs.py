#!/usr/bin/env python3

#BoBoBo#

import yaml
import os
import json
import importlib
import requests
from pin.kit.common import get_conf


ss = None


def reset(servs_cfg_path):
    global ss
    try:
        with open(servs_cfg_path, mode='r') as ss:
            ss = yaml.load(ss, Loader=yaml.CLoader)
    except Exception as ex:
        print('Failed to reset servs cfg for: ' + str(ex))
        ss = None


cfg = get_conf('engine')
reset(cfg('pin', 'servs'))


def get_serv(path):

    server_cfg = None

    def _remote_serv(*args, **kw):
        nonlocal path
        nonlocal server_cfg

        if None is server_cfg:
            raise Exception('None server cfg.')

        url = 'http://' + server_cfg['host'] + \
            ':' + str(server_cfg['port']) + path
        resp = requests.post(url, json=kw)
        return resp.json()

    global ss
    if None is path or '' == path:
        return None
    else:
        elems = path.split('/')[1:]

        y = ss['servs']
        for e in elems:
            y = y[e]

        module_path = y['module']
        server_cfg = y['server']
        try:
            module = importlib.import_module(module_path)
        except Exception as ex:
            print('Warning: Failed to import local servs moudle: ' +
                  module_path + ' for: ' + str(ex))
            print('Use remote servs to: ' + path)
            return _remote_serv
        else:
            fn = getattr(module, elems[-1])
            return fn


def just_data(resp):
    if 'content' in resp:
        content = json.loads(resp['content'])
    if 'errCode' in resp:
        content = resp
    return content['errCode'], content.get('errMsg', None), content.get('data', None)
