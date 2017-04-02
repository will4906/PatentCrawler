# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
import time

from entity.ItemData import ItemData
from enums.Config import Config
from util.excel.ExcelUtil import ExcelUtil


class CollectionResult:
    PATENT_TYPE = ["发明申请", "实用新型", "外观设计"]

    def __init__(self, progressInfo):
        self.__itemDataList = []
        self.__initItemDataList()
        self.__progressInfo = progressInfo

    def __initItemDataList(self):
        sh = ExcelUtil(Config.FILE_NAME).getSheet(0, "read")
        for i in range(1, sh.nrows):
            item = ItemData()
            item.set_patent_type(sh.cell(i, 0).value)
            item.set_name(sh.cell(i, 1).value)
            item.set_law_state(sh.cell(i, 2).value)
            item.set_law_state_date(sh.cell(i, 3).value)
            item.set_announcement_date(sh.cell(i, 4).value)
            item.set_request_number(sh.cell(i, 5).value)
            item.set_request_date(sh.cell(i, 6).value)
            item.set_proposer_name(sh.cell(i, 7).value)
            item.set_inventor_name(sh.cell(i, 8).value)
            self.__itemDataList.append(item)

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
            hasSameRequestNumber = False
            for i in range(len(self.__itemDataList)):
                if self.__itemDataList[i].get_request_number() == itemData.get_request_number():
                    hasSameRequestNumber = True
                    strOldDate = self.__itemDataList[i].get_law_state_date()
                    strNewDate = itemData.get_law_state_date()
                    if strOldDate == "无数据" or strNewDate == "无数据":
                        newAnnouncementDate = time.strftime("%Y%m%d", time.strptime(itemData.get_announcement_date(), '%Y.%m.%d'))
                        oldAnnouncementDate = time.strftime("%Y%m%d", time.strptime(self.__itemDataList[i].get_announcement_date(), '%Y.%m.%d'))
                        if int(newAnnouncementDate) > int(oldAnnouncementDate):
                            self.__itemDataList[i] = itemData
                            self.__writeToExcel(i + 1, itemData.get_patent_type(), itemData.get_name(),
                                                itemData.get_law_state(), itemData.get_law_state_date(),
                                                itemData.get_announcement_date(),
                                                itemData.get_request_number(), itemData.get_request_date(),
                                                itemData.get_proposer_name(), itemData.get_inventor_name())
                            print(
                                itemData.get_patent_type() + "\t" + itemData.get_name() + "\t" + itemData.get_type() + "\t" + itemData.get_request_number() + "\t" + itemData.get_request_date() + "\t" + itemData.get_announcement_date() + "\t" + itemData.get_proposer_name() + "\t" + itemData.get_inventor_name() + "\t" + itemData.get_law_state() + "\t" + itemData.get_law_state_date() + "\t" + "更新")
                            break
                    elif int(itemData.get_law_state_date()) > int(self.__itemDataList[i].get_law_state_date()):
                        self.__itemDataList[i] = itemData
                        self.__writeToExcel(i + 1, itemData.get_patent_type(), itemData.get_name(),
                                            itemData.get_law_state(), itemData.get_law_state_date(),
                                            itemData.get_announcement_date(),
                                            itemData.get_request_number(), itemData.get_request_date(),
                                            itemData.get_proposer_name(), itemData.get_inventor_name())
                        print(
                            itemData.get_patent_type() + "\t" + itemData.get_name() + "\t" + itemData.get_type() + "\t" + itemData.get_request_number() + "\t" + itemData.get_request_date() + "\t" + itemData.get_announcement_date() + "\t" + itemData.get_proposer_name() + "\t" + itemData.get_inventor_name() + "\t" + itemData.get_law_state() + "\t" + itemData.get_law_state_date() + "\t" + "更新")
                        break

            if not hasSameRequestNumber:
                self.__itemDataList.append(itemData)
                print(
                    itemData.get_patent_type() + "\t" + itemData.get_name() + "\t" + itemData.get_type() + "\t" + itemData.get_request_number() + "\t" + itemData.get_request_date() + "\t" + itemData.get_announcement_date() + "\t" + itemData.get_proposer_name() + "\t" + itemData.get_inventor_name() + "\t" + itemData.get_law_state() + "\t" + itemData.get_law_state_date())
                self.__writeToExcel(len(self.__itemDataList), itemData.get_patent_type(), itemData.get_name(),
                                    itemData.get_law_state(), itemData.get_law_state_date(),
                                    itemData.get_announcement_date(),
                                    itemData.get_request_number(), itemData.get_request_date(),
                                    itemData.get_proposer_name(), itemData.get_inventor_name())

    def __writeToExcel(self, index, patentType, name, lawState, lawStateDate, aDate, requestNumber, requestDate, proposerName,
                       inventorName):
        try:
            editor = ExcelUtil(Config.FILE_NAME).edit()
            sh = editor.getSheet(0)
            sh.write(index, 0, patentType)
            sh.write(index, 1, name)
            sh.write(index, 2, lawState)
            sh.write(index, 3, lawStateDate)
            sh.write(index, 4, aDate)
            sh.write(index, 5, requestNumber)
            sh.write(index, 6, requestDate)
            sh.write(index, 7, proposerName)
            sh.write(index, 8, inventorName)
            editor.commit()
        except Exception as e:
            print("写excel报错")
            Config.writeLog("写excel报错")
            Config.writeException(e)
