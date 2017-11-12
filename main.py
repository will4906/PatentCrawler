# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import time
import os
import sys

from scrapy import cmdline

from config.BaseConfig import BaseConfig
from config.LoginInfo import LoginInfo
from entity.models import Patents
from service.CookieService import CookieService
from service.LoginService import LoginService
from util.excel.ExcelUtil import ExcelUtil


def initProgress():
    if CookieService.readCookies() is False:
        print('未读取到保存的cookie')
    else:
        print('读取到保存的cookie，然而并没有什么用网站设置了不让记住账号，每次都得重新登录')
    try:
        os.mkdir("output")
    except Exception as e:
        pass
    try:
        os.mkdir("log")
    except:
        pass
    try:
        os.mkdir("temp_save")
    except:
        pass


def checkForConfig():
    if LoginInfo.USERNAME == '':
        LoginInfo.USERNAME = input('未填写账号，请填写：')
    if LoginInfo.PASSWORD == '':
        LoginInfo.PASSWORD = input('未填写密码，请填写：')


def init_excel_config():
    title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "公布号", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人", "IPC分类号",
                  "代理人", "代理机构", "外观设计洛迦诺分类号"]
    editor = ExcelUtil(BaseConfig.FILE_NAME).edit()
    sh = editor.getSheet(0)
    for index, each in enumerate(title_list):
        sh.write(0, index, each)
    editor.commit()
    return


def initDataBase():
    Patents.create_table()

if __name__ == '__main__':
    print("程序开始")
    print(
        "* 使用说明：https://github.com/will4906/PatentCrawler/wiki\n* 代码更新：https://github.com/will4906/PatentCrawler\n* bug反馈、交流建议：\n邮箱：553105821@qq.com\ngithub：https://github.com/will4906/PatentCrawler/issues")
    initProgress()
    initDataBase()
    # LoginService().startLogin()
    checkForConfig()
    init_excel_config()
    cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + BaseConfig.LOG_FILE_NAME).split())
    print("cmdline")
