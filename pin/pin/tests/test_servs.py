#!/usr/bin/env python3

#BoBoBo#

from threading import Thread
import time
import pin.kit.rpc.servs as servs
import pin.embed.server as server
from pin.router import *


def test_local():
    code, msg, data = servs.just_data(
        servs.get_serv('/test/serv/local')(param1=1, param2=2))
    assert code == 0
    assert data == 'param1=1,param2=2'


def local(param1, param2):
    data = 'param1=' + str(param1) + ',' + 'param2=' + str(param2)
    result = {'errCode': 0, 'errMsg': 'succeed', 'data': data}
    return result


@route("/test/serv/remote")
def remote(param1, param2):
    data = 'param1=' + str(param1) + ',' + 'param2=' + str(param2)
    result = {'errCode': 0, 'errMsg': 'succeed', 'data': data}
    return result


app = pin_app(True)


def test_remote():
    global app
    t = Thread(target=server.bootstrap, args=(app,), daemon=True)
    t.start()
    print("Waiting server start for 5 seconds...")
    time.sleep(5)

    code, msg, data = servs.just_data(
        servs.get_serv('/test/serv/remote')(param1=3, param2=4))
    assert code == 0
    assert data == 'param1=3,param2=4'
