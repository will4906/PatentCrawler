# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
description = (
    '''
    用户信息配置模块
    
    由于专利网站的改版，现在要求必须要登录账号密码才能进行高级查询，
    请使用者到专利网站自行注册账号，并修改一下USERNAME和PASSWORD的值
    链接：http://www.pss-system.gov.cn/sipopublicsearch/portal/uiregister-showRegisterPage.shtml
    '''
)


# 账号
import click


USERNAME = ''
# 密码
PASSWORD = ''


def check_username(cfg):
    """
    校验用户名
    :param cfg:
    :return:
    """
    global USERNAME
    index = 0
    while True:
        try:
            username = str(cfg['account']['username'])
            username = username.replace(' ','')
            if username == '':
                raise Exception('username invalid')
            else:
                USERNAME = username
            break
        except:
            if index == 0:
                click.echo(description)
            index += 1
            username = click.prompt('未填写用户名，请填写')
            username = username.replace(' ', '')
            if username != '':
                USERNAME = username
                break


def check_password(cfg):
    """
    校验密码
    :param cfg:
    :return:
    """
    global PASSWORD
    while True:
        try:
            password = cfg['account']['password']
            if password == '':
                raise Exception('password invalid')
            else:
                PASSWORD = password
            break
        except:
            password = click.prompt('未填写密码，请填写')
            if password != '':
                PASSWORD = password
                break
