# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from entity.query_item import title_define


class ItemCollection:

    @staticmethod
    def resolveData(item, title, itemvalue):
        for key, value in title_define.items():
            if title.find(value) != -1:
                item[key] = itemvalue
                break

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
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'targetProposer')
        ItemCollection.addSingleCrawlerItemValue(item, temp, 'targetInventor')


    @staticmethod
    def addSingleCrawlerItemValue(item, temp, key):
        strTmp = temp.get(key)
        if strTmp != None and strTmp != 'None':
            item[key] = strTmp
