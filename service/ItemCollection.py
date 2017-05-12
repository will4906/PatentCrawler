# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""


class ItemCollection:

    @staticmethod
    def resolveData(item, strTemp):
        if strTemp.find("申请号") != -1:
            item['requestNumber'] = strTemp[6:]
        elif strTemp.find("申请日") != -1:
            item['requestDate'] = strTemp[5:]
        elif strTemp.find("公告") != -1 and strTemp.find("日") != -1:
            item['publishDate'] = strTemp[9:]
        elif strTemp.find("公告") != -1 and strTemp.find("号") != -1:
            item['publishNumber'] = strTemp[10:]
        elif strTemp.find("申请") != -1 and strTemp.find("人") != -1:
            item['proposerName'] = strTemp[10:-1]
        elif strTemp.find("发明人") != -1:
            item['inventorName'] = strTemp[5:-1]
        elif strTemp.find("代理人") != -1:
            item['agent'] = strTemp[5:-1]
        elif strTemp.find("代理机构") != -1:
            item['agency'] = strTemp[6:-1]
        elif strTemp.find("IPC分类号") != -1:
            item['ipcNumber'] = strTemp[8:-1]
        elif strTemp.find("外观设计洛迦诺分类号") != -1:
            item['locarnoNumber'] = strTemp[12:]
        else:
            return

    @staticmethod
    def addCrawlerItem(item, temp):
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'name')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'type')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'patentType')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'requestNumber')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'requestDate')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'publishDate')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'publishNumber')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'proposerName')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'inventorName')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'ipcNumber')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'agent')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'agency')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'locarnoNumber')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'lawState')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'lawStateDate')


    @staticmethod
    def addSingleCrawlerItemValue(item, temp, key):
        strTmp = temp.get(key)
        if strTmp != None and strTmp != 'None':
            item[key] = strTmp
