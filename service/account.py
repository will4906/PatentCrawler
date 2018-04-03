import base64
import configparser

import click
import requests
from logbook import *
# from requests.cookies import RequestsCookieJar

import controller as ctrl

from config.base_settings import CAPTCHA_MODEL_NAME, TIMEOUT, USE_PROXY
from controller.url_config import url_captcha, url_login
# from service.log import init_log
from service.proxy import update_proxy, notify_ip_address, update_cookies
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
    resp = requests.get(url=url_captcha.get('url'), cookies=ctrl.COOKIES, proxies=ctrl.PROXIES)
    with open('captcha.png', 'wb') as f:
        f.write(resp.content)
    result = get_captcha_result(CAPTCHA_MODEL_NAME, 'captcha.png')
    return result


def check_login_status():
    if USE_PROXY:
        try:
            if ctrl.PROXIES is not None:
                notify_ip_address()
                logger.info('当前已有登录状态')
                return True
        except:
            pass
    return False


def login(username=None, password=None):
    """
    登录API
    :return: True: 登录成功; False: 登录失败
    """
    if username is None or password is None:
        username = account.username
        password = account.password
    ctrl.BEING_LOG = True
    if check_login_status():
        ctrl.BEING_LOG = False
        return True

    error_times = 0
    while True:
        try:
            # logger.debug("before proxy")
            update_proxy()
            # logger.debug("before cookie")
            update_cookies()
            # logger.debug("after cookie")
            busername = change_to_base64(username)
            bpassword = change_to_base64(password)
            captcha = get_captcha()
            logger.info('验证码识别结果：%s' % captcha)
            form_data = url_login.get('form_data')
            form_data.__setitem__('j_validation_code', captcha)
            form_data.__setitem__('j_username', busername)
            form_data.__setitem__('j_password', bpassword)

            resp = requests.post(url=url_login.get('url'), headers=url_login.get('headers'), data=form_data,
                                 cookies=ctrl.COOKIES, proxies=ctrl.PROXIES, timeout=TIMEOUT)
            if resp.text.find(username + '，欢迎访问') != -1:
                # 网站调整了逻辑，下面这句不用了
                # print(resp.cookies)
                # ctrl.COOKIES.__delitem__('IS_LOGIN')
                # ctrl.COOKIES.set('IS_LOGIN', 'true', domain='www.pss-system.gov.cn/sipopublicsearch/patentsearch')
                jsession = ctrl.COOKIES.get('JSESSIONID')
                resp.cookies.__delitem__('JSESSIONID')
                resp.cookies.set('JSESSIONID', jsession, domain='www.pss-system.gov.cn')
                update_cookies(resp.cookies)
                requests.post(
                    'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml',
                    cookies=ctrl.COOKIES, proxies=ctrl.PROXIES)
                ctrl.BEING_LOG = False
                logger.info('登录成功')
                return True
            else:
                if error_times > 5:
                    break
                logger.error('登录失败')
                error_times += 1
        except Exception as e:
            logger.error(e)

    ctrl.BEING_LOG = False
    return False


if __name__ == '__main__':
    pass
    # init_log()
    # login('', '')
    # print(notify_ip_address())
    # # resp = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml', cookies=ctrl.COOKIES)
    # # print(resp.text)
    # form_data = url_detail.get('form_data')
    # # '''
    # # 'nrdAn': '',
    # #     'cid': '',
    # #     'sid': '',
    # #     'wee.bizlog.modulelevel': '0201101'
    # # '''
    # form_data.__setitem__('nrdAn', 'CN201520137687')
    # form_data.__setitem__('cid', 'CN201520137687.320150916XX')
    # form_data.__setitem__('sid', 'CN201520137687.320150916XX')
    # print(ctrl.COOKIES)
    # resp = requests.post(url_detail.get('url'), headers=url_detail.get('headers'), cookies=ctrl.COOKIES, data=form_data)
    # print(resp.text)
