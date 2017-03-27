# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from entity.ItemData import ItemData
from util.LawState import LawState
from util.WaitEngine import WaitEngine


class ItemCollection:
    def __init__(self, driver, pageCollection, patentType, whichItem):
        self.__item_data = ItemData()
        self.__item_data.set_patent_type(patentType)
        self.__driver = driver
        self.__waitEngine = WaitEngine(driver)
        self.__pageCollection = pageCollection
        self.__whichItem = whichItem

    def collectingData(self):
        try:
            name = self.collecting_name()
            self.__item_data.set_name(name)
            type = self.collecting_type()
            self.__item_data.set_type(type)
            if name != "" and type != "":
                pLen = self.__driver.execute_script("return document.getElementsByClassName(\"item-content-body\")[" + str(self.__whichItem) + "].children.length;")
                for i in range(pLen):
                    strData = self.__driver.execute_script("return document.getElementsByClassName(\"item-content-body\")[" + str(self.__whichItem) + "].children[" + str(i) + "].innerText;")
                    strTemp = str(strData)
                    if strTemp.find("申请号") != -1:
                        requestNumber = strTemp[7:]
                        self.__item_data.set_request_number(requestNumber)
                    elif strTemp.find("申请日") != -1:
                        requestDate = strTemp[6:]
                        self.__item_data.set_request_date(requestDate)
                    elif strTemp.find("公告") != -1 and strTemp.find("日") != -1:
                        announcement_date = strTemp[10:]
                        self.__item_data.set_announcement_date(announcement_date)
                    elif strTemp.find("申请") != -1 and strTemp.find("人") != -1:
                        proposer_name = strTemp[11:-2]
                        self.__item_data.set_proposer_name(proposer_name)
                    elif strTemp.find("发明人") != -1:
                        inventor_name = strTemp[6:-2].replace('\n', '')
                        self.__item_data.set_inventor_name(inventor_name)
                print("准备收集法律信息")
                LawState(self.__driver, self).collecting_law_state(self.__whichItem)
            else:
                self.__pageCollection.collectingItemSuccessfullyWithOutData()
        except:
            self.__pageCollection.collectingItemUnsuccessfully()
            return False

    def collectingLawDataSuccessfully(self, lawUpdate, lawState):
        print("采集法律信息成功")
        self.__item_data.set_law_state(lawState)
        self.__item_data.set_law_state_date(lawUpdate)
        self.__pageCollection.collectingItemSuccessfully(self.__item_data)

    def collectingLawDataUnsuccessfully(self):
        print("收集法律信息失败")
        self.__pageCollection.collectingItemUnsuccessfully()

    def get_item_data(self):
        return self.__item_data

    # 收集一个数据
    def __collecting_one_data(self, str_script):
        try:
            data = self.__driver.execute_script(str_script)
            return data
        except:
            return None

    # 处理一个元素
    def __deal_with_element(self, str_script):
        try:
            self.__driver.execute_script(str_script)
            return True
        except:
            return False

    # 专利名称
    def collecting_name(self):
        name = self.__collecting_one_data("return document.getElementsByName(\"titleHidden\").item(" + str(
                    self.__whichItem) + ").attributes.getNamedItem(\"value\").textContent;")
        if name is not None:
            self.__item_data.set_name(name)
        return self.__item_data.get_name()

    # 公告或授权公告类型
    def collecting_type(self):
        type = self.__collecting_one_data("return document.getElementsByClassName(\"item-header\").item(" + str(
            self.__whichItem) + ").childNodes.item(3).childNodes.item(3).textContent;")
        if type is not None:
            self.__item_data.set_type(type)
        return self.__item_data.get_type()
