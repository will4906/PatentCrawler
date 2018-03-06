# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import configparser
import shutil
import os
import sys

import click
from scrapy import cmdline

from config import account_settings as account
from config import base_settings as base
from config.base_settings import *
# from visual.map_charts import ChinaMap
from entity.models import Patents
from service.log import init_log


def init_config():
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join('config', 'config.ini'), 'utf-8')
    account.check_username(cfg)
    account.check_password(cfg)
    base.check_proxy(cfg)
    base.check_request(cfg)
    base.check_output(cfg)
    # print(base.TIMEOUT)


def init_base_path():
    if os.path.exists(OUTPUT_PATH) is False:
        os.mkdir(OUTPUT_PATH)
    if os.path.exists(OUTPUT_GROUP_PATH) is False:
        os.mkdir(OUTPUT_GROUP_PATH)
    shutil.copy(TEMPLATE_NAME, DIAGRAM_NAME)


def init_data_base():
    Patents.create_table()


if __name__ == '__main__':
    click.echo(
        '''
***************************************************************************
* 使用说明：https://github.com/will4906/PatentCrawler/wiki
* 代码更新：https://github.com/will4906/PatentCrawler
* bug反馈、交流建议:
* \t邮箱：553105821@qq.com
* \tgithub：https://github.com/will4906/PatentCrawler/issues
***************************************************************************
        '''
    )
    init_log()
    init_config()
    init_base_path()
    init_data_base()
    # print(base.OUTPUT_ITEMS)
    if 'log' in base.OUTPUT_ITEMS:
        cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + LOG_FILENAME).split())
    else:
        cmdline.execute(("scrapy crawl Patent").split())

