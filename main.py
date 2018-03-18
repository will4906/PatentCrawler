# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import configparser
import os
import sys

import click
from scrapy import cmdline

from config import base_settings as base
from config.base_settings import *
# from crawler.pipelines import CrawlerPipeline
from entity.models import Patents
from service.account import account
from service.info import init_crawler
from service.log import init_log


def init_config():
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join('config', 'config.ini'), 'utf-8')
    account.check_username(cfg)
    account.check_password(cfg)
    base.check_proxy(cfg)
    base.check_request(cfg)
    base.check_output(cfg)
    init_crawler(cfg)


def init_base_path():
    if os.path.exists(OUTPUT_PATH) is False:
        os.mkdir(OUTPUT_PATH)
    if os.path.exists(OUTPUT_GROUP_PATH) is False:
        os.mkdir(OUTPUT_GROUP_PATH)


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
    init_base_path()
    init_config()

    # init_data_base()
    # CrawlerPipeline().process_item(None, None)
    if 'log' in base.OUTPUT_ITEMS:
        cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + LOG_FILENAME).split())
    else:
        cmdline.execute(("scrapy crawl Patent").split())

