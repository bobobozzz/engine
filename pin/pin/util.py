#!/usr/bin/env python3

#BoBoBo#

import configparser
import logging

errcode_ret = lambda (code, msg, data) : {'errCode': code, 'errMsg': msg, 'data': data}
err_code = lambda errcode_ret : errcode_ret['errCode']
err_msg = lambda errcode_ret : errcode_ret['errMsg']
ret_data = lambda errcode_ret : errcode_ret['data']

conf = load_conf()
logger = get_logger()

def get_conf(section, key, default):
    try:
        return conf.get(section, key)
    except configparser.Error:
        logger.warning('Found No config of %s : %s' % (section, key))
        return default

def load_conf(conf_path = 'etc/app.conf'):
    conf = configparser.ConfigParser()
    if conf_path[0] == '/':
        conf_file = conf_path
    else:
        conf_file = os.getcwd() + '/'  + conf_path
    conf.read(conf_file)

def get_logger():
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
    except BaseError:
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
