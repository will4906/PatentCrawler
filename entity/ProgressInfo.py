# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from entity.CollectionResult import CollectionResult
from entity.QueryInfo import QueryInfo


class ProgressInfo:
    def __init__(self):
        self.__queryInfo = QueryInfo()
        self.__inventorIndex = 0
        self.__patentTypeIndex = 0
        self.__pageSum = 0
        self.__pageIndex = 1
        self.__itemIndex = 0
        self.__collectionResult = CollectionResult(self)

    def getQueryInfo(self):
        return self.__queryInfo

    def getCollectionResult(self):
        return self.__collectionResult

    def setCollectionResult(self, connectionResult = None):
        self.__collectionResult = connectionResult

    def getInventorIndex(self):
        return self.__inventorIndex

    def setInventorIndex(self, inventorIndex):
        self.__inventorIndex = inventorIndex

    def getPatentTypeIndex(self):
        return self.__patentTypeIndex

    def setPatentTypeIndex(self, patentTypeIndex):
        self.__patentTypeIndex = patentTypeIndex

    def getPageSum(self):
        return self.__pageSum

    def setPageSum(self, pageSum):
        self.__pageSum = pageSum

    def getPageIndex(self):
        return self.__pageIndex

    def setPageIndex(self, pageIndex):
        self.__pageIndex = pageIndex

    def getItemIndex(self):
        return self.__itemIndex

    def setItemIndex(self, itemIndex):
        self.__itemIndex = itemIndex