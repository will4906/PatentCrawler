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


def init_base_path():
    if os.path.exists(OUTPUT_PATH) is False:
        os.mkdir(OUTPUT_PATH)
    if os.path.exists(OUTPUT_GROUP_PATH) is False:
        os.mkdir(OUTPUT_GROUP_PATH)
    shutil.copy(TEMPLATE_NAME, DIAGRAM_NAME)


# def checkForConfig():
#     if LoginInfo.USERNAME == '':
#         LoginInfo.USERNAME = input('未填写账号，请填写：')
#     if LoginInfo.PASSWORD == '':
#         LoginInfo.PASSWORD = input('未填写密码，请填写：')
#
#
# def init_excel_config():
#     worksheet = XlsxUtil(EXCEL_NAME).getWorksheet()
#     # title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "公布号", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人", "IPC分类号",
#     #               "代理人", "代理机构", "外观设计洛迦诺分类号"]
#     # editor = ExcelUtil(BaseConfig.FILE_NAME).edit()
#     # sh = editor.getSheet(0)
#     # for index, each in enumerate(title_list):
#     #     sh.write(0, index, each)
#     # editor.commit()
#     return
#
#
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

    cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + LOG_FILENAME).split())

