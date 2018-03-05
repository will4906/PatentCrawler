import base64

import requests
from logbook import *
from requests import ReadTimeout

import controller as ctrl

from config.account_settings import USERNAME, PASSWORD
from config.base_settings import CAPTCHA_MODEL_NAME, TIMEOUT, USE_PROXY
from controller.url_config import url_captcha, url_index, url_login
from service.proxy import update_proxy, check_proxy, notify_ip_address
from service.request import get, post
from service.sipoknn import get_captcha_result

logger = Logger(__name__)


@check_proxy
def update_cookies(cookies=None):
    """
    更新或获取cookies
    :param cookies:
    :return:
    """

    if cookies is None:
        ctrl.COOKIES = requests.get(url=url_index.get('url'), proxies=ctrl.PROXIES, timeout=TIMEOUT).cookies
    else:
        ctrl.COOKIES = cookies

    logger.info(ctrl.COOKIES)
    if len(ctrl.COOKIES) == 0:
        logger.error('cookie有问题')
        raise ReadTimeout('cookie有问题')


def change_to_base64(source):
    """
    将参数进行base64加密
    :param source:
    :return:
    """
    return str(base64.b64encode(bytes(source, encoding='utf-8')), 'utf-8')


def get_captcha():
    """
    获取验证码
    :return:
    """
    index = 0
    while True:
        resp = get(url=url_captcha.get('url'), cookies=ctrl.COOKIES, proxies=ctrl.PROXIES)
        with open('captcha.png', 'wb') as f:
            f.write(resp.content)
        try:
            index += 1
            result = get_captcha_result(CAPTCHA_MODEL_NAME, 'captcha.png')
            return result
        except OSError as e:
            logger.error('验证码获取失败，尝试重试，重试次数%s' % index)
            update_proxy()


def login():
    """
    登录API
    :return: True: 登录成功; False: 登录失败
    """
    ctrl.BEING_LOG = True
    if USE_PROXY:
        try:
            if ctrl.PROXIES is not None:
                notify_ip_address()
                logger.info('当前已有登录状态')
                ctrl.BEING_LOG = False
                return True
            else:
                update_proxy()
        except:
            update_proxy()

    update_cookies()
    username = change_to_base64(USERNAME)
    password = change_to_base64(PASSWORD)
    for i in range(3):
        captcha = get_captcha()
        logger.info('验证码识别结果：%s' % captcha)
        form_data = url_login.get('form_data')
        form_data.__setitem__('j_validation_code', captcha)
        form_data.__setitem__('j_username', username)
        form_data.__setitem__('j_password', password)
        resp = post(url=url_login.get('url'), headers=url_login.get('headers'), data=form_data)
        if resp.text.find(USERNAME + '，欢迎访问') != -1:
            update_cookies(resp.cookies)
            ctrl.BEING_LOG = False
            logger.info('登录成功')
            return True
        else:
            logger.error('登录失败')
    ctrl.BEING_LOG = False
    return False


def relogin_when_error(func):
    """
    报错重新登录的装饰器，暂时无用
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == 'relogin':
            update_cookies()
            login()

    return wrapper


if __name__ == '__main__':
    pass
    # logger.info('hello world')
    # print(__name__)
    # update_cookies()
    # print(login())
