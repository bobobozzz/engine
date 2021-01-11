#!/usr/bin/env python3

#BoBoBo#

from pin.kit.tester.asserter import t_yaml


def test_t():

    tyaml = """
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
            skip-send-login-smscode:
                skip: !!bool true
                asserts: # This is parameter standard of pin.kit.tester .
                    - asserter: !!python/module:pin.kit.tester.mysql_asserter
                      cfg: *mysql
                      param:
                        assert-not-empty: "select 1"
    """
    t_yaml(tyaml)
