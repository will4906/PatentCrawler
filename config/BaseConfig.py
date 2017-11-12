# -*- coding: utf-8 -*-
"""
Created on 2017/5/12

@author: will4906
"""
from util.TimeUtil import TimeUtil


class BaseConfig:
    # 爬取专利速度，每个请求80个，范围是(0,89]
    CRAWLER_SPEED = "12"
    FILE_NAME = "output\专利.xls"
    OUT_PUT_DIR = 'output\\'
    LOG_FILE_NAME = "log\PatentCrawler{0}.log".format(TimeUtil.getFormatTime("%Y%m%d_%H%M%S"))
    TEMP_DIR_NAME = "temp_save"

    # 发明人名称检查
    CHECK_INVENTOR = True
    # 申请人名称检查
    CHECK_PROPOSER = True