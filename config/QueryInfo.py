# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""


class SearchNameDefine:
    REQUEST_NUMBER = '申请号'
    REQUEST_DATE = '申请日'
    PUBLISH_NUMBER = '公开（公告）号'
    PUBLISH_DATE = '公开（公告）日'
    PROPOSER_NAME = '申请（专利权）人'
    INVENTOR_NAME = '发明人'
    PRIORITY_NUMBER = '优先权号'
    PRIORITY_DATE = '优先权日'
    ABSTRACT = '摘要'
    CLAIM = '权利要求'
    INSTRUCTIONS = '说明书'
    KEY_WORD = '关键词'


class QueryInfo:
    def __init__(self):
        self.__inventionTypeList = ["I", "U", "D"]
        self.__inventorList = ["陈思平", "陈昕", "汪天富", "谭力海", "彭珏", "但果", "叶继伦", "覃正笛",
                               "张旭", "张会生", "钱建庭", "丁惠君", "刁现芬", "沈圆圆", "周永进", "孔湉湉",
                               "陆敏华", "张新宇", "孙怡雯", "李乔亮", "齐素文", "徐海华", "倪东", "刘维湘",
                               "李抱朴", "黄炳升", "徐敏", "雷柏英", "胡亚欣", "何前军", "郑介志", "常春起",
                               "陈雯雯", "罗永祥", "黄鹏", "林静", "王倪传", "刘立", "张治国", "董磊"]
        self.__proposer = "深圳大学"
        # self.__inventorList = [""]
        # self.__proposer = "北京科技大学"
        self.__startDate = "2001-01-01"
        return

    def getInventionTypeList(self):
        return self.__inventionTypeList

    @staticmethod
    def inventionTypeToString(type):
        if type == "I":
            return "发明申请"
        elif type == "U":
            return "实用新型"
        elif type == "D":
            return "外观设计"

    def getInventorList(self):
        return self.__inventorList

    def getProposer(self):
        return self.__proposer

    def getStartDate(self):
        return self.__startDate

    def setStartDate(self, startDate):
        self.__startDate = startDate
