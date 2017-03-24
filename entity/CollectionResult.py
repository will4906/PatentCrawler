# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""


class CollectionResult:

    PATENT_TYPE = ["发明申请", "实用新型", "外观设计"]

    def __init__(self):
        self.__itemDataList = []

    def getItemDataList(self):
        return self.__itemDataList
