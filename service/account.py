import base64
import configparser

import click
import requests
from logbook import *
from requests import ReadTimeout

import controller as ctrl

from config.base_settings import CAPTCHA_MODEL_NAME, TIMEOUT, USE_PROXY
from controller.url_config import url_captcha, url_index, url_login
from service.proxy import update_proxy, check_proxy, notify_ip_address
from service.request import get, post
from service.sipoknn import get_captcha_result

logger = Logger(__name__)


account_notify_times = 0
description = (
    '''
    用户信息配置模块

    由于专利网站的改版，现在要求必须要登录账号密码才能进行高级查询，
    请使用者到专利网站自行注册账号，并修改一下USERNAME和PASSWORD的值
    链接：http://www.pss-system.gov.cn/sipopublicsearch/portal/uiregister-showRegisterPage.shtml
    '''
)


class Account:
    """
    账户信息定义
    """
    def __init__(self):
        # 用户名，约定私有约束，使用请调用self.username
        self._username = ''
        # 密码，约定私有约束，使用请调用self.password
        self._password = ''

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        if username is None:
            raise Exception('username invalid')
        username = username.replace(' ', '')
        if username == '':
            raise Exception('username invalid')
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if password is None or password == '':
            raise Exception('password invalid')
        self._password = password

    def check_username(self, cfg: configparser.ConfigParser):
        """
        用户名校验，设置
        :param cfg:
        :return:
        """
        try:
            username = cfg.get('account', 'username')
            self.username = username
        except:
            click.echo(description)
            while True:
                try:
                    username = click.prompt('用户名出错，请填写')
                    self.username = username
                    break
                except:
                    pass

    def check_password(self, cfg: configparser.ConfigParser):
        """
        密码校验，配置
        :param cfg:
        :return:
        """
        try:
            password = cfg.get('account', 'password')
            self.password = password
        except:
            while True:
                try:
                    password = click.prompt('密码出错，请填写')
                    self.password = password
                    break
                except:
                    pass


# 账户信息的单例
account = Account()


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
    username = change_to_base64(account.username)
    password = change_to_base64(account.password)
    for i in range(3):
        captcha = get_captcha()
        logger.info('验证码识别结果：%s' % captcha)
        form_data = url_login.get('form_data')
        form_data.__setitem__('j_validation_code', captcha)
        form_data.__setitem__('j_username', username)
        form_data.__setitem__('j_password', password)
        resp = post(url=url_login.get('url'), headers=url_login.get('headers'), data=form_data)
        if resp.text.find(account.username + '，欢迎访问') != -1:
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

