# -*- coding: utf-8 -*-
"""
Created on 2017/4/1

@author: will4906
"""
import time


class TimeUtil:

    @staticmethod
    def getFormatTime(strFormat):
        return time.strftime(strFormat,time.localtime(time.time()))