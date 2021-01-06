#!/usr/bin/env python3

#BoBoBo#

import pytest
from pin.kit.tester.http_asserter import assert_keys


def test_assert_keys():
    e1 = {'e1': 1, 'e2': 'a', 'e3': False, 'e4': None, 'e5': '!!ignore!!'}
    e2 = {'e1': 1, 'e2': 'a', 'e3': False, 'e4': None, 'e5': []}
    e3 = {'e1': 1, 'e2': 'b', 'e3': False, 'e4': None, 'e5': []}

    d1 = {'k1': 1, 'k2': 'a', 'k3': False, 'k4': None, 'k5': [e1], 'k6': e1}
    d2 = {'k1': 1, 'k2': 'a', 'k3': False, 'k4': None, 'k5': [e2], 'k6': e1}
    d3 = {'k1': 1, 'k2': 'a', 'k3': False, 'k4': None, 'k5': [e1], 'k6': e2}
    d4 = {'k1': 1, 'k2': 'a', 'k3': False, 'k4': None, 'k5': [e3], 'k6': e1}

    assert assert_keys(d1, d2)
    assert assert_keys(d1, d3)

    with pytest.raises(AssertionError) as e:
        assert_keys(d1, d4)
    assert 'Different string: b' == str(e.value)
