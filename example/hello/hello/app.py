#!/usr/bin/env python3

#BoBoBo#

from pin.controller import dispatch
import .controller

def engine(request):
    return dispatch(request)
