# -*- coding: utf-8 -*-
"""
Created on 2017/3/27

@author: will4906
"""

import xlwt
import xlrd
from xlutils.copy import copy

from util.excel.ExcelEditor import ExcelEditor

import xlsxwriter


class XlsxUtil:
    def __init__(self, filename):
        self.workbook = xlsxwriter.Workbook(filename)

    def getWorksheet(self):
        return self.workbook.add_worksheet()

class ExcelUtil:

    def __init__(self, filename):
        self.__fileName = filename
        try:
            xlrd.open_workbook(filename)
        except:
            work_book = xlwt.Workbook()
            work_sheet = work_book.add_sheet("Sheet1")
            work_book.save(filename)

    def getExcel(self, mode):           # 采用工厂模式建立excel的读写实例
        if isinstance(mode, str):
            if mode.upper() == "READ":
                return xlrd.open_workbook(self.__fileName)
            elif mode.upper() == "WRITE":
                rb = xlrd.open_workbook(self.__fileName)
                return copy(rb)
        else:
            return None

    # 添加表
    def addSheet(self, sheet):
        return self.getExcel("WRITE").add_sheet(sheet)

    # 获取表
    def getSheet(self, which, mode):
        try:
            wb = self.getExcel(mode)
            if isinstance(which, str):
                if mode.upper() == "READ":
                    return wb.sheet_by_name(which)
                else:
                    return None
            elif isinstance(which, int):
                if mode.upper() == "READ":
                    return wb.sheet_by_index(which)
                elif mode.upper() == "WRITE":
                    return wb.get_sheet(which)
                else:
                    return None
            else:
                return None
        except Exception as e:
            print("excel报错-------------------------------" + str(e))
            return

    # 调用这个方法生成editor,主要模仿安卓的SharedPreferences
    def edit(self):
        wb = self.getExcel("write")
        return ExcelEditor(wb, self.__fileName)
