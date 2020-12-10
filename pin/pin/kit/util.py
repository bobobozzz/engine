#!/usr/bin/env python3

#BoBoBo#

import configparser
import logging
import os


def errcode_ret(code, msg, data): return {
    'errCode': code, 'errMsg': msg, 'data': data}


def err_code(errcode_ret): return errcode_ret['errCode']
def err_msg(errcode_ret): return errcode_ret['errMsg']
def ret_data(errcode_ret): return errcode_ret['data']


def load_conf(conf_path='etc/pin.conf'):
    conf = configparser.ConfigParser()
    if conf_path[0] == '/':
        conf_file = conf_path
    else:
        conf_file = os.getcwd() + '/' + conf_path

    if os.path.exists(conf_file):
        conf.read(conf_file)
    else:
        try:
            conf_file = os.environ['PIN_CONF']
        except KeyError:
            print('Failed to load conf file by environ var PIN_CONF.')
        else:
            if os.path.exists(conf_file):
                conf.read(conf_file)
            else:
                print('Failed to load conf file.')
    return conf


conf = load_conf()


def get_section(section):
    global conf
    try:
        m = conf[section]
        n = map(lambda v: int(v) if v.isnumeric() else v, m.values())
        return dict(zip(m, n))
    except KeyError:
        return None


def get_conf(section, key, default=None):
    try:
        s = conf.get(section, key)
        if s.isnumeric():
            try:
                return int(s)
            except ValueError:
                return float(s)
        else:
            return s
    except configparser.Error:
        logger.warning('Found No config of %s : %s' % (section, key))
        return default
    except Exception:
        logger.warning('Invalid value of %s : %s' % (section, key))
        return None


def get_logger():
    global conf
    try:
        level = conf.get('log', 'level')
    except configparser.Error:
        level = logging.INFO

    try:
        log_file = conf.get('log', 'log_path')
    except configparser.Error:
        log_file = 'log.txt'

    try:
        form = conf.get('log', 'pattern')
        formatter = logging.Formatter(form)
    except Exception:
        form = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(form)

    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(level)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = get_logger()


def html_escape(string):
    """ Escape HTML special characters ``&<>`` and quotes ``'"``. """
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                 .replace('"', '&quot;').replace("'", '&#039;')


def assertNotNone(*params):
    if all(params):
        return True
    else:
        raise Exception('Error Parameter')
