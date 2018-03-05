# -*- coding: utf-8 -*-
"""
Created on 2018/2/27

@author: will4906
"""
import logging
import requests

import controller as ctrl
from service.account import *
from service.proxy import check_proxy


logging.getLogger(__name__).setLevel(logging.DEBUG)


@check_proxy
def get(*args, **kwargs):
    return request(request_type='get', **kwargs)


@check_proxy
def post(*args, **kwargs):
    return request(request_type='post', **kwargs)


def request(*args, **kwargs):
    request_type = kwargs.pop('request_type')
    kwargs.__setitem__('proxies', ctrl.PROXIES)
    kwargs.__setitem__('cookies', ctrl.COOKIES)
    kwargs.__setitem__('timeout', TIMEOUT)
    if request_type == 'get':
        return requests.get(**kwargs)
    elif request_type == 'post':
        return requests.post(**kwargs)
    else:
        raise Exception("Can't read the requests type")
