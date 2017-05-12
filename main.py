# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import time
import os
import sys

from enums.Config import Config
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
    title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人"]
    editor = ExcelUtil(Config.FILE_NAME).edit()
    sh = editor.getSheet(0)
    for index, each in enumerate(title_list):
        sh.write(0, index, each)
    editor.commit()
    return


if __name__ == '__main__':
    print(int(6/9))
    for index in range(1, 1):
        print(1)
    # initProgress()
    # 这句非常重要，提高python的递归深度，否则递归900次就炸了
    # sys.setrecursionlimit(1000000)  # 例如这里设置为一百万
    # startDate = input("请输入公布日开始日期,如{0}：".format(TimeUtil.getFormatTime("%Y-%m-%d")))
    # Config.writeLog("程序启动，输入的公布开始日期为{0}".format(startDate))
    # init_excel_config()
    #
    # progress = ProgressController(Config.BROSWER_NAME)
    # Config.writeLog("启动{0}浏览器".format(Config.BROSWER_NAME))
    # queryInfo = progress.getQueryInfo()
    # queryInfo.setStartDate(startDate)
    #
    # progress.startProgress()

    # print(excel)
