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
            type = self.collecting_type()
            if name != "" and type != "":
                pLen = self.__driver.execute_script("return document.getElementsByClassName(\"item-content-body\")[" + str(self.__whichItem) + "].children.length;")
                for i in range(pLen):
                    strData = self.__driver.execute_script("return document.getElementsByClassName(\"item-content-body\")[" + str(self.__whichItem) + "].children[" + str(i) + "].innerText;")
                    strTemp = str(strData)
                    if strTemp.find("申请号") != -1:
                        requestNumber = strTemp[7:]
                    elif strTemp.find("申请日") != -1:
                        requestDate = strTemp[6:]
                    elif strTemp.find("公告") != -1 and strTemp.find("日") != -1:
                        announcement_date = strTemp[10:]
                    elif strTemp.find("申请") != -1 and strTemp.find("人") != -1:
                        proposer_name = strTemp[11:-2]
                    elif strTemp.find("发明人") != -1:
                        inventor_name = strTemp[6:-2]
                law_state = self.collecting_law_state()
                print(self.__item_data.get_patent_type() + "\t" + name + "\t" + type[
                                                         1:-1] + "\t" + requestNumber + "\t" + requestDate + "\t" + announcement_date + "\t" + proposer_name + "\t" + inventor_name + "\t" + law_state)
            self.__pageCollection.collectingItemSuccessfully(self.__item_data)
        except:
            self.__pageCollection.collectingItemUnsuccessfully()
            return False

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

    # 法律信息
    def collecting_law_state(self):
        law_state = LawState(self.__driver).collecting_law_state(self.__whichItem)
        if law_state is not None:
            self.__item_data.set_law_state(law_state)
        return self.__item_data.get_law_state()