#!/usr/bin/env python3

#BoBoBo#

from pin.kit.tester.asserter import test_by_yaml


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
    test_by_yaml(tests_yaml)
