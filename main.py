# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import time

from controller.ProgressController import ProgressController
from enums.Config import Config
from util.excel.ExcelUtil import ExcelUtil


def init_excel_config():
    title_list = ["专利类型", "专利名称", "法律状态", "法律状态最后修改日期", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人"]
    editor = ExcelUtil(Config.FILE_NAME).edit()
    sh = editor.getSheet(0)
    for index, each in enumerate(title_list):
        sh.write(0, index, each)
    editor.commit()
    return

if __name__ == '__main__':
    init_excel_config()

    progress = ProgressController("Chrome")
    progress.startProgress()

    # print(excel)


