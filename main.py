# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import time

import xlwt

from controller.ProgressController import ProgressController


def init_excel_config(date):
    title_list = ["专利类型", "专利名称", "法律状态", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人"]
    work_book = xlwt.Workbook()
    work_sheet = work_book.add_sheet("Sheet1")
    for index, each in enumerate(title_list):
        work_sheet.write(0, index, each)
    work_book.save("专利({0}).xls".format(date))
    return work_book, work_sheet

if __name__ == '__main__':
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    init_excel_config(date)

    progress = ProgressController()
    progress.startProgress()


