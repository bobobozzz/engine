#!/usr/bin/env python3

#BoBoBo#

from pin.view import *


def test_tpl_path():
    path = tpl_path()
    assert not None is path
