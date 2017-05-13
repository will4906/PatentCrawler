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
from util.excel.ExcelUtil import ExcelUtil


def initProgress():
    try:
        os.mkdir("output")
    except Exception as e:
        pass
    try:
        os.mkdir("log")
    except:
        pass


def init_excel_config():
    title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "公布号", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人", "IPC分类号", "代理人", "代理机构", "外观设计洛迦诺分类号"]
    editor = ExcelUtil(BaseConfig.FILE_NAME).edit()
    sh = editor.getSheet(0)
    for index, each in enumerate(title_list):
        sh.write(0, index, each)
    editor.commit()
    return


# 第页 共 10 页 721 条数据
if __name__ == '__main__':
    # startDate = input("请输入公布日开始日期,如{0}：".format(TimeUtil.getFormatTime("%Y-%m-%d")))
    # Config.writeLog("程序启动，输入的公布开始日期为{0}".format(startDate))
    print("程序开始")
    initProgress()
    init_excel_config()
    cmdline.execute(("scrapy crawl Patent -s LOG_FILE=" + BaseConfig.LOG_FILE_NAME).split())
    # 共 1 页   5条数据
    # 第页 共 10 页 721 条数据
    # str = "第页 共 10 页 721 条数据"
    # s = str[2:].find("页")
    # e = str.find("条")
    # print(s)
    # print(e)
    # print(int(str[str[2:].find("页") + 3:str.find("条")]))


