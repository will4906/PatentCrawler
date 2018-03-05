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


# def request_login(func):
#     """
#     报错重新登录的装饰器，暂时无用
#     :param func:
#     :return:
#     """
#     def wrapper(*args, **kwargs):
#         resp = func(*args, **kwargs)
#         if resp.text.find('window.location.href = contextPath +"/portal/uilogin-forwardLogin.shtml";') != -1:
#             login_status = False
#             while login_status is False:
#                 try:
#                     update_proxy()
#                     update_cookies()
#                     login_status = login()
#                     if login_status:
#                         logging.info('登录成功')
#                     else:
#                         logging.info('登录失败')
#                 except Exception as e:
#                     logging.exception(e)
#
#     return wrapper


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
