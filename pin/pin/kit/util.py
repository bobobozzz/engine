#!/usr/bin/env python3

#BoBoBo#

import logging

from pin.kit.common import get_conf


def get_logger(conf=None):
    if not conf:
        conf = get_conf(None)

    level = conf('log', 'level', logging.INFO)
    log_file = conf('log', 'log_path', 'log.txt')

    default_form = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    form = conf('log', 'pattern', default_form)
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


def html_escape(string):
    """ Escape HTML special characters ``&<>`` and quotes ``'"``. """
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                 .replace('"', '&quot;').replace("'", '&#039;')


def assertNotNone(*params):
    if all(params):
        return True
    else:
        raise Exception('Error Parameter')
