# -*- coding: utf-8 -*-
"""
Created on 2017/3/29

@author: will4906
"""
from util.FileUtil import FileUtil
from util.TimeUtil import TimeUtil


class Config:
    BROSWER_NAME = "PhantomJs"
    LOG_FILE_NAME = "log\PatentCrawler{0}.log".format(TimeUtil.getFormatTime("%Y%m%d_%H%M%S"))
    FILE_NAME = "output\专利.xls"
    REJECT_WAY = "您的操作太过频繁，已被网站限制操作\n应对方式：\n(1)重启路由器;\n(2)拔掉网线重新连接;\n(3)重启电脑\n(4)通知管理员采取应对办法"
    AND_STRING = "………………………………………………"

    @staticmethod
    def writeLog(strLog):
        FileUtil(Config.LOG_FILE_NAME, "a+").writeLine(
            TimeUtil.getFormatTime("%Y/%m/%d-%H:%M:%S") + Config.AND_STRING + strLog)

    @staticmethod
    def writeException(strException):
        FileUtil(Config.LOG_FILE_NAME, "a+").writeLine(str(strException))
