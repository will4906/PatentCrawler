# -*- coding: utf-8 -*-
"""
Created on 2017/5/12

@author: will4906
"""


class BaseConfig:
    # 爬取专利速度，每个请求80个，范围是(0,89]
    CRAWLER_SPEED = "80"
    FILE_NAME = "output\专利.xls"