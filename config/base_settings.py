# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

一下地址、文件名可根据用户使用自行修改，工程所有地址将会采用。
"""
import os

from util.TimeUtil import TimeUtil

# 工程根目录，注意此处以初次调用这个变量的元素为准，工程起始目录定位在main，若有修改请注意这个位置
BASE_PATH = os.getcwd() + os.sep
# 输出目录
OUTPUT_PATH = BASE_PATH + 'output'
# 输出分组，默认按年月日_时分秒分组
OUTPUT_GROUP_PATH = OUTPUT_PATH + os.sep + TimeUtil.getFormatTime('%Y%m%d_%H%M%S')
# 采集存放数据库地址
DATABASE_NAME = OUTPUT_GROUP_PATH + os.sep + 'Patent.db'
# 生成excel地址
EXCEL_NAME = OUTPUT_GROUP_PATH + os.sep + '专利.xlsx'
# 生成图表地址
DIAGRAM_NAME = OUTPUT_GROUP_PATH + os.sep + 'diagram.html'
# log输出目录
LOG_PATH = BASE_PATH + 'log'
# log文件名
LOG_FILENAME = LOG_PATH + os.sep + "PatentCrawler{0}.log".format(TimeUtil.getFormatTime("%Y%m%d_%H%M%S"))
# 模板文件目录，不建议修改
TEMPLATE_PATH = BASE_PATH + 'res' + os.sep + 'template'
# 模板文件地址，有可能增加和改变，不建议修改
TEMPLATE_NAME = TEMPLATE_PATH + os.sep + 'template.html'