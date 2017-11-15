# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import shutil
import time
import os
import sys

from scrapy import cmdline

from config.LoginInfo import LoginInfo
from entity.models import Patents
from service.CookieService import CookieService
from service.LoginService import LoginService
from util.excel.ExcelUtil import ExcelUtil, XlsxUtil
from config.base_settings import OUTPUT_PATH, OUTPUT_GROUP_PATH, LOG_PATH, BASE_PATH, TEMPLATE_NAME, DIAGRAM_NAME, \
    DATABASE_NAME, LOG_FILENAME, EXCEL_NAME
from visual.map_charts import ChinaMap


def initPath():
    if os.path.exists(OUTPUT_PATH) is False:
        os.mkdir(OUTPUT_PATH)
    if os.path.exists(OUTPUT_GROUP_PATH) is False:
        os.mkdir(OUTPUT_GROUP_PATH)
    if os.path.exists(LOG_PATH) is False:
        os.mkdir(LOG_PATH)
    shutil.copy(TEMPLATE_NAME, DIAGRAM_NAME)
    # 调试临时添加，待会改掉
    # shutil.copy('G:\Core\python\workspace\PatentCrawler\\visual\\ai.db', DATABASE_NAME)


def checkForConfig():
    if LoginInfo.USERNAME == '':
        LoginInfo.USERNAME = input('未填写账号，请填写：')
    if LoginInfo.PASSWORD == '':
        LoginInfo.PASSWORD = input('未填写密码，请填写：')


def init_excel_config():
    worksheet = XlsxUtil(EXCEL_NAME).getWorksheet()
    # title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "公布号", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人", "IPC分类号",
    #               "代理人", "代理机构", "外观设计洛迦诺分类号"]
    # editor = ExcelUtil(BaseConfig.FILE_NAME).edit()
    # sh = editor.getSheet(0)
    # for index, each in enumerate(title_list):
    #     sh.write(0, index, each)
    # editor.commit()
    return


def initDataBase():
    Patents.create_table()

if __name__ == '__main__':
    print("程序开始")
    print(
        "* 使用说明：https://github.com/will4906/PatentCrawler/wiki\n"
        "* 代码更新：https://github.com/will4906/PatentCrawler\n"
        "* bug反馈、交流建议：\n"
        "\t邮箱：553105821@qq.com\n"
        "\tgithub：https://github.com/will4906/PatentCrawler/issues")
    initPath()
    initDataBase()
    checkForConfig()
    cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + LOG_FILENAME).split())
