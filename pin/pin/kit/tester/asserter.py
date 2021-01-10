#!/usr/bin/env python3

#BoBoBo#

import yaml
import pytest
from pin.kit.tester import *


def test_by_yaml(tests_yaml):
    try:
        tests = yaml.load(tests_yaml, Loader=yaml.CLoader)
    except Exception:
        pytest.fail("Wrong tests yaml.")

    test_servs = tests["test-servs"]
    list(map(lambda k: t_case(test_servs[k]), test_servs))


def t_case(serv):
    asserts = serv["asserts"]
    list(map(lambda a: do_assert(a), asserts))


def do_assert(a):
    asserter = a["asserter"]
    asserter.t(a)
