# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""


# 一个item应采集的数据bean
class ItemData:

    def __init__(self):
        self.__name = ""  # 专利名称
        self.__patent_type = ""  # 专利类型（发明申请，外观设计，实用新型）
        self.__type = ""  # 类型（公告，授权公告）
        self.__request_number = ""  # 申请号
        self.__request_date = ""  # 申请日
        self.__announcement_date = ""  # 公告日
        self.__proposer_name = ""  # 申请人
        self.__inventor_name = ""  # 发明人
        self.__law_state = ""  # 法律状态
        return

    def set_name(self, name):
        self.__name = name

    def set_patent_type(self, patent_type):
        self.__patent_type = patent_type

    def set_type(self, type):
        self.__type = type

    def set_request_number(self, request_number):
        self.__request_number = request_number

    def set_request_date(self, request_date):
        self.__request_date = request_date

    def set_announcement_date(self, announcement_date):
        self.__announcement_date = announcement_date

    def set_proposer_name(self, proposer_name):
        self.__proposer_name = proposer_name

    def set_inventor_name(self, inventor_name):
        self.__inventor_name = inventor_name

    def set_law_state(self, law_state):
        self.__law_state = law_state

    def get_name(self):
        return self.__name

    def get_patent_type(self):
        return self.__patent_type

    def get_type(self):
        return self.__type

    def get_request_number(self):
        return self.__request_number

    def get_request_date(self):
        return self.__request_date

    def get_announcement_date(self):
        return self.__announcement_date

    def get_proposer_name(self):
        return self.__proposer_name

    def get_inventor_name(self):
        return self.__inventor_name

    def get_law_state(self):
        return self.__law_state