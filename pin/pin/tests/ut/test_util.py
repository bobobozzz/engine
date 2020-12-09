#!/usr/bin/env python3

#BoBoBo#

import pytest
from pin.kit.util import *


def test_util():
    with pytest.raises(Exception, match="Error Parameter"):
        assertNotNone(None)
    assert assertNotNone(1) is True
    with pytest.raises(Exception, match="Error Parameter"):
        assert assertNotNone(1, None, 2) is False
