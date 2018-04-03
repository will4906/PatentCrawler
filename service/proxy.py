# -*- coding: utf-8 -*-
"""
Created on 2018/2/25

@author: will4906

代理模块

程序的代理决定使用https://github.com/jhao104/proxy_pool的代理池作为代理方式，

开发者可以修改下方get_proxy函数进行自定义
"""
import json

from logbook import Logger
from requests.exceptions import RequestException, ReadTimeout

import controller as ctrl
import requests

from config import base_settings as bs
from controller.url_config import url_pre_execute, url_index

logger = Logger(__name__)


def notify_ip_address():
    """
    通知专利网我们的ip地址，
    这个网站比较特别，每当有陌生ip地址时，都需要通过这个方法向网站发送一次请求先。
    :return:
    """
    resp = requests.post(url_pre_execute.get('url'), proxies=ctrl.PROXIES, timeout=bs.TIMEOUT, cookies=ctrl.COOKIES)
    # logger.debug(resp.text)
    ip_address = json.loads(resp.text)
    if ctrl.PROXIES is not None:
        if ip_address.get('IP') == ctrl.PROXIES.get('http').split(':')[0]:
            return resp.text
        else:
            raise Exception('ip error')
    else:
        return resp.text


def get_proxy():
    """
    获取代理ip，并更新控制器PROXIES
    :return: 可用的ip代理
    """
    if bs.USE_PROXY is False:
        return None

    try:
        logger.info('获取代理···')
        resp = requests.get(bs.PROXY_URL, timeout=bs.TIMEOUT)
        ip_address = resp.text
        proxies = {'http': ip_address, 'https': ip_address}
        logger.info(proxies)
        ctrl.PROXIES = proxies
        return ctrl.PROXIES
    except Exception as e:
        logger.error('无法获取代理信息，请确认代理系统是否启动')
        return None


def update_proxy():
    """
    获取并校验代理ip地址
    :return:
    """
    if bs.USE_PROXY:
        i = 0
        while True:
            try:
                get_proxy()
                notify_ip_address()
                return True
            except Exception:
                i += 1
                logger.error("代理获取失败，尝试重试，重试次数%s" % (i, ))
    else:
        logger.info('notify address')
        notify_ip_address()


def update_cookies(cookies=None):
    """
    更新或获取cookies
    :param cookies:
    :return:
    """
    if cookies is None:
        ctrl.COOKIES = requests.get(url=url_index.get('url'), proxies=ctrl.PROXIES, timeout=bs.TIMEOUT).cookies

    else:
        ctrl.COOKIES = cookies

    logger.info(ctrl.COOKIES)
    if len(ctrl.COOKIES) == 0:
        logger.error('cookie有问题')
        raise ReadTimeout('cookie有问题')


def check_proxy(func):
    """
    校验代理的装饰器，使用情况较特殊，只针对请求超时异常
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                resp = func(*args, **kwargs)
                return resp
            except RequestException:
                update_proxy()
        raise Exception('函数重试5次，仍无法成功')
    return wrapper


if __name__ == '__main__':
    print(update_proxy())
    # update_cookies()
    # print(login())
