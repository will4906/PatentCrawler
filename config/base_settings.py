# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

基础路径模块

以下地址、文件名可根据用户使用自行修改，工程所有地址将会采用。
"""
import os

from util.TimeUtil import TimeUtil

"""
路径设置
"""
# 工程根目录，注意此处以初次调用这个变量的元素为准，工程起始目录定位在main，若有修改请注意这个位置
BASE_PATH = os.path.split(os.path.split(__file__)[0])[0]
# 输出目录
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
# 输出分组，默认按年月日_时分秒分组
OUTPUT_GROUP_PATH = os.path.join(OUTPUT_PATH, TimeUtil.getFormatTime('%Y%m%d_%H%M%S'))
# 采集存放数据库地址
DATABASE_NAME = os.path.join(OUTPUT_GROUP_PATH, 'Patent.db')
# 生成excel地址
EXCEL_NAME = os.path.join(OUTPUT_GROUP_PATH, '专利.xlsx')
# 生成图表地址
DIAGRAM_NAME = os.path.join(OUTPUT_GROUP_PATH, 'diagram.html')
# log输出目录
LOG_PATH = os.path.join(BASE_PATH, 'log')
# log文件名
LOG_FILENAME = os.path.join(LOG_PATH, "PatentCrawler{0}.log".format(TimeUtil.getFormatTime("%Y%m%d_%H%M%S")))
# 模板文件目录，不建议修改
TEMPLATE_PATH = os.path.join(BASE_PATH, 'res', 'template')
# 模板文件地址，有可能增加和改变，不建议修改
TEMPLATE_NAME = os.path.join(TEMPLATE_PATH, 'template.html')
# 验证码模型地址
CAPTCHA_MODEL_NAME = os.path.join(BASE_PATH, 'res', 'captcha', 'sipoknn.job')

"""
基础设置
"""
# 是否使用代理
USE_PROXY = True
# 请求超时，单位秒
TIMEOUT = 10
