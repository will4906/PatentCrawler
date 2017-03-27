# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""


class CollectionResult:

    PATENT_TYPE = ["发明申请", "实用新型", "外观设计"]

    def __init__(self, progressInfo):
        self.__itemDataList = []
        self.__progressInfo = progressInfo

    def getItemDataList(self):
        return self.__itemDataList

    def addItem(self, itemData):
        queryInfo = self.__progressInfo.getQueryInfo()
        inventorList = itemData.get_inventor_name().split(";")
        hasInventor = False
        for inventor in inventorList:
            if queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()] == inventor.strip():
                hasInventor = True
                break
        if hasInventor == True:
            hasSameName = False
            for i in range(len(self.__itemDataList)):
                if self.__itemDataList[i].get_name() == itemData.get_name():
                    hasSameName = True
                    if int(itemData.get_law_state_date()) > int(self.__itemDataList[i].get_law_state_date()):
                        self.__itemDataList[i] = itemData
                        break
            if not hasSameName:
                self.__itemDataList.append(itemData)
                print(
                    itemData.get_patent_type() + "\t" + itemData.get_name() + "\t" + itemData.get_type() + "\t" + itemData.get_request_number() + "\t" + itemData.get_request_date() + "\t" + itemData.get_announcement_date() + "\t" + itemData.get_proposer_name() + "\t" + itemData.get_inventor_name() + "\t" + itemData.get_law_state() + "\t" + itemData.get_law_state_date())
                # self.__pageCollection.collectingItemSuccessfully(self.__item_data)