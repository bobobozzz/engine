#!/usr/bin/env python3

#BoBoBo#

'''
Common Appointments
'''

import configparser
import os

PROTOCOL_KEY_CODE = 'errCode'
PROTOCOL_KEY_MESSAGE = 'errMsg'
PROTOCOL_KEY_DATA = 'data'

PROTOCOL_CODE_SUCCESS = 0
PROTOCOL_CODE_FAIL = 1
PROTOCOL_CODE_NOTHING = 5


def protocol_succeed(data):
    if data:
        return {
            PROTOCOL_KEY_CODE: PROTOCOL_CODE_SUCCESS,
            PROTOCOL_KEY_DATA: data
        }
    else:
        return {
            PROTOCOL_KEY_CODE: PROTOCOL_CODE_SUCCESS,
        }


def protocol_nothing():
    return {
        PROTOCOL_KEY_CODE: PROTOCOL_CODE_NOTHING,
    }


def protocol_fail(msg, data=None):
    if data:
        return {
            PROTOCOL_KEY_CODE: PROTOCOL_CODE_FAIL,
            PROTOCOL_KEY_MESSAGE: msg,
            PROTOCOL_KEY_DATA: data
        }
    else:
        return {
            PROTOCOL_KEY_CODE: PROTOCOL_CODE_FAIL,
            PROTOCOL_KEY_MESSAGE: msg
        }


def errcode_ret(code, msg, data): return {
    PROTOCOL_KEY_CODE: code, PROTOCOL_KEY_MESSAGE: msg, PROTOCOL_KEY_DATA: data}


def err_code(errcode_ret): return errcode_ret[PROTOCOL_KEY_CODE]
def err_msg(errcode_ret): return errcode_ret[PROTOCOL_KEY_MESSAGE]
def ret_data(errcode_ret): return errcode_ret[PROTOCOL_KEY_DATA]


def decide_conf_file(hint_path='./etc/pin.conf'):
    if hint_path:
        if hint_path[0] == '/':
            conf_file = conf_path
        else:
            conf_file = os.getcwd() + '/' + hint_path

        if os.path.exists(conf_file):
            return conf_file
    try:
        conf_file = os.environ['PIN_CONF']
    except KeyError:
        print('No environ var: PIN_CONF.')
    else:
        if os.path.exists(conf_file):
            return conf_file

    print('Found no conf file.')
    return None


def get_conf(app_name, conf_file=None):
    conf_file = decide_conf_file(conf_file)
    conf = configparser.ConfigParser()
    try:
        conf.read(conf_file)
    except:
        print("Failed to read conf file: " + str(conf_file))
        conf = None

    def _get_conf(section, key, default=None):
        nonlocal conf
        nonlocal app_name
        try:
            if conf is None:
                raise Exception('None conf.')

            if app_name and '' != app_name:
                section = app_name + '.' + section
            s = conf.get(section, key)
            if s.isnumeric():
                try:
                    return int(s)
                except ValueError:
                    return float(s)
            else:
                return s
        except configparser.Error:
            print('Found No config of %s:%s' %
                  (section, key) + '. Will use default.')
            return default
        except Exception as e:
            print('Faild to get value %s : %s' %
                  (section, key) + ' Exception: ' + str(e))
            return default

    return _get_conf
