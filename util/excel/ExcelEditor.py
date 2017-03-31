# -*- coding: utf-8 -*-
"""
Created on 2017/3/28

@author: will4906
"""


# 模仿安卓SharedPreferences生成editer进行写入操作
class ExcelEditor:

    def __init__(self, wb, fileName):
        self.__workBook = wb
        self.__fileName = fileName

    # 各种写操作执行完之后，一定要调用这个方法保存
    def commit(self):
        self.__workBook.save(self.__fileName)

    def getSheet(self, index):
        return self.__workBook.get_sheet(index)