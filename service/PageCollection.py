# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from entity.CollectionResult import CollectionResult
from enums.Config import Config
from service.ItemCollection import ItemCollection


class PageCollection:
    def __init__(self, progressController, collectionResult):
        self.__progressController = progressController
        self.__collectionResult = collectionResult
        self.__driver = progressController.getWebDriver()
        self.__itemLength = 0
        self.__itemIndex = 0
        self.__patentTypeIndex = 0

    def startCollecting(self, patentTypeIndex, startItemIndex=0):
        self.__itemLength = 0
        self.__patentTypeIndex = patentTypeIndex
        self.__itemIndex = startItemIndex
        try:
            self.__itemLength = self.__driver.execute_script("return document.getElementsByClassName(\"item\").length;")
        except Exception as e:
            Config.writeException(e)
            print(e)
            self.__itemLength = 0
            self.__progressController.collectingUnsuccessfully()
            return False
        if self.__itemIndex < self.__itemLength:
            Config.writeLog("开始收集")
            itemCollectiong = ItemCollection(self.__driver, self, CollectionResult.PATENT_TYPE[patentTypeIndex],
                                             self.__itemIndex)
            itemCollectiong.collectingData()
        else:
            Config.writeLog("收集失败")
            print("收集失败")
            self.__progressController.collectingUnsuccessfully(self.__itemIndex)
        Config.writeLog("itemIndex = {0}".format(self.__itemIndex))
        return True

    def collectingItemSuccessfully(self, itemData):
        Config.writeLog("采集item成功")
        self.__collectionResult.addItem(itemData)
        self.__itemIndex += 1
        Config.writeLog("采集item成功itemIndex = {0}, itemLength = {1}".format(self.__itemIndex, self.__itemLength))
        if self.__itemIndex < self.__itemLength:
            itemCollectiong = ItemCollection(self.__driver, self, CollectionResult.PATENT_TYPE[self.__patentTypeIndex],
                                             self.__itemIndex)
            itemCollectiong.collectingData()
        else:
            self.__progressController.collectingSuccessfully()

    def collectingItemSuccessfullyWithOutData(self):
        Config.writeLog("采集空item成功")
        self.__itemIndex += 1
        if self.__itemIndex < self.__itemLength:
            itemCollectiong = ItemCollection(self.__driver, self, CollectionResult.PATENT_TYPE[self.__patentTypeIndex],
                                             self.__itemIndex)
            itemCollectiong.collectingData()
        else:
            self.__progressController.collectingSuccessfully()

    def collectingItemUnsuccessfully(self):
        print("采集item失败")
        Config.writeLog("采集item失败")
        self.__progressController.collectingUnsuccessfully(self.__itemIndex)
