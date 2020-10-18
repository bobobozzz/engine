#!/usr/bin/env python3

#BoBoBo#

from pin.controller import dispatch
import controller

def engine(request):
    return dispatch(request)

#Run just by python with embed server.
if __name__ == "__main__":
    import pin.embed.server as server
    server.bootstrap()
