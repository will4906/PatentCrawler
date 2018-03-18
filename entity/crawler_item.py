# -*- coding: utf-8 -*-
"""
Created on 2018/3/13

@author: will4906
"""
import configparser

from bs4 import BeautifulSoup
from logbook import Logger

logger = Logger(__name__)

id_preview = 0          # 预览页
id_detail = 1           # 细节页
id_cognation = 2        # 同族页
# id_
crawler_list = {
    id_preview: {},
    id_detail: {},
    id_cognation: {},
}


class BaseItem:
    # 是否必须参数，即无论用户在config.ini如何配置都会进行采集记录
    is_required = False
    # 在url_config.py对应的url标志
    crawler_id = -1
    # 采集结果对应的中文名称
    chinese = None
    # 采集结果对应的英文名称
    english = None
    # 字段标题
    title = None
    # 隶属表名称
    table_name = 'main'
    # 字段名称
    field_names = None

    @classmethod
    def set_title(cls, title):
        if cls.title is None:
            cls.title = title

    @classmethod
    def get_chinese(cls):
        """
        如果中文为字符串，则直接返回，若为list则返回第一个元素
        :return:
        """
        if isinstance(cls.chinese, str):
            return cls.chinese
        elif isinstance(cls.chinese, list):
            return str(cls.chinese[0])

    @classmethod
    def check_chinese(cls, chinese):
        if isinstance(cls.chinese, str):
            if chinese == cls.chinese:
                return True
            else:
                return False
        elif isinstance(cls.chinese, list):
            if chinese in cls.chinese:
                cls.chinese = chinese
                return True
            else:
                return False

    @classmethod
    def check_english(cls, english):
        if isinstance(cls.english, str):
            if english == cls.english:
                return True
            else:
                return False
        elif isinstance(cls.english, list):
            if english in cls.english:
                cls.english = english
                return True
            else:
                return False

    @classmethod
    def get_english(cls):
        """
        如果英文为字符串，则直接返回，若为list则返回第一个元素
        :return:
        """
        if isinstance(cls.english, str):
            return cls.english
        elif isinstance(cls.english, list):
            return str(cls.english[0])

    @classmethod
    def parse(cls, raw, item, process=None):
        """
        数据解析函数
        :param raw: 原生内容
        :param item: scarpy采集的item
        :param process: 如果非json则传递BeautifulSoup对象
        :return:
        """
        pass


class ResultItem:
    """
    储存采集结果的对象
    """
    def __init__(self, table='main', title=None, value=None):
        self.table = table
        self.title = title
        self.value = value

    def __repr__(self):
        return str(self.__dict__)
