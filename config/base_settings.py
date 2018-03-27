# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

基础路径模块

以下地址、文件名可根据用户使用自行修改，工程所有地址将会采用。
"""
import configparser
import os

import click

from util.TimeUtil import TimeUtil

"""
路径设置
"""
# 工程根目录，注意此处以初次调用这个变量的元素为准，工程起始目录定位在main，若有修改请注意这个位置
BASE_PATH = os.path.split(os.path.split(__file__)[0])[0]
# 输出目录
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
# 输出分组，默认按年月日_时分秒分组
OUTPUT_GROUP_PATH = os.path.join(OUTPUT_PATH, TimeUtil.getFormatTime('%Y%m%d_%H%M%S'))
# 采集存放数据库地址
DATABASE_NAME = os.path.join(OUTPUT_GROUP_PATH, 'Patent.db')
# 生成excel地址
EXCEL_NAME = os.path.join(OUTPUT_GROUP_PATH, '专利.xlsx')
# 生成图表目录
CHARTS_NAME = os.path.join(OUTPUT_GROUP_PATH, 'charts.html')
# log文件名
LOG_FILENAME = os.path.join(OUTPUT_GROUP_PATH, "PatentCrawler.log")
# 验证码模型地址
CAPTCHA_MODEL_NAME = os.path.join(BASE_PATH, 'res', 'captcha', 'sipo3.job')
# 赞赏html路径
AD_PATH = os.path.join(BASE_PATH, 'res', 'advertisement', 'ad.html')

"""
基础设置
"""
# 是否使用代理
USE_PROXY = False
# 代理请求url，若USE_PROXY为False则忽略此项
PROXY_URL = 'http://127.0.0.1:5010/get'
# 请求超时，单位秒
TIMEOUT = 10
# 请求延时，单位秒
DOWNLOAD_DELAY = 1
# 输出项目
OUTPUT_ITEMS = ['data', 'log', 'chart']


def check_proxy(cfg):
    """
    检查代理相关信息
    :param cfg:
    :return:
    """
    global USE_PROXY
    try:
        use_proxy = cfg.getboolean('proxy', 'use_proxy')
        USE_PROXY = use_proxy
    except:
        click.echo('代理配置异常，使用默认值')

    if USE_PROXY:
        try:
            proxy_url = cfg['proxy']['proxy_url']
            if proxy_url != '':
                global PROXY_URL
                PROXY_URL = proxy_url
            else:
                raise Exception('proxy error')
        except:
            click.echo('代理url配置异常，使用默认值')


def check_request(cfg: configparser.ConfigParser):
    """
    检查请求相关信息
    :param cfg:
    :return:
    """
    global TIMEOUT
    global DOWNLOAD_DELAY
    try:
        timeout = cfg.getint('request', 'timeout')
        if timeout > 0:
            TIMEOUT = timeout
        else:
            raise Exception('timeout error')
    except:
        click.echo('timeout配置异常，使用默认值')

    try:
        delay = cfg.getfloat('request', 'delay')
        if delay > 0:
            DOWNLOAD_DELAY = delay
        else:
            raise Exception('delay error')
    except:
        click.echo("延时配置异常，使用默认值")


def check_output(cfg):
    """
    检查输出相关信息
    :return:
    """
    global OUTPUT_ITEMS
    try:
        output_items = str(cfg.get('output', 'items'))
        output_items = output_items.replace(' ', '')
        output_item_list = output_items[1:-1].split(',')
        result = ''
        for item in output_item_list:
            result += "'" + item + "',"
        result = output_items[0] + result + output_items[-1]
        output_items = eval(result)
        if isinstance(output_items, list):
            OUTPUT_ITEMS = output_items
        else:
            raise Exception('items error')
    except Exception as e:
        click.echo('输出内容配置异常，使用默认值')
