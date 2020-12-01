#!/usr/bin/env python3

#BoBoBo#

import pytest
import yaml


def test_t():

    tests_yaml = """
        mysql: &mysql
            host: engine.test.mysql
            port: 3306
            database: db_test
            user: test
            password: test
        test-servs:
            # Test Case
            succeed-send-login-smscode:
                asserts: # This is parameter standard of pin.kit.tester .
                    - asserter: !!python/module:pin.kit.tester.mysql_asserter
                      cfg: *mysql
                      param:
                        assert-not-empty: "select 2"
    """
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
