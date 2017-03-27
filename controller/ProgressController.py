# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
import os

import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from entity.ProgressInfo import ProgressInfo
from service.Connection import Connection
from service.PageCollection import PageCollection
from service.Query import Query
from selenium import webdriver


class ProgressController:
    def __init__(self):
        # self.__driver = webdriver.PhantomJS(executable_path='.\\res\phantomjs.exe')
        # self.__driver = webdriver.Chrome()

        binary = FirefoxBinary(r'C:\Software\MozillaFirefox\firefox.exe')
        self.__driver = webdriver.Firefox(firefox_binary=binary)

        # self.__driver.set_page_load_timeout(120)        # firefox会报错
        self.__connection = Connection(self)
        self.__query = Query(self)
        self.__progressInfo = ProgressInfo()
        self.__pageCollection = PageCollection(self, self.__progressInfo.getCollectionResult())
        return

    def getWebDriver(self):
        return self.__driver

    def startProgress(self):
        try:
            self.__connection.connectUrl()
        except Exception as e:
            print(e)

    def loadUrlSuccessfully(self):
        print("成功连接url")
        queryInfo = self.__progressInfo.getQueryInfo()
        inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
        proposer = queryInfo.getProposer()
        startDate = queryInfo.getStartDate()
        patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
        self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)

    def loadUrlUnsuccessfully(self):
        print("url连接失败")
        self.__connection.refreshUrl()

    def queryTargetSuccessfully(self, pageSum):
        print("检索成功")
        self.__progressInfo.setPageSum(pageSum)

        if pageSum == 0:
            print("pageSum = 0")
            self.__progressInfo.setItemIndex(0)
            self.__progressInfo.setPageIndex(1)
            self.__progressInfo.setPatentTypeIndex(0)
            inventorIndex = self.__progressInfo.getInventorIndex() + 1
            self.__progressInfo.setInventorIndex(inventorIndex)

            queryInfo = self.__progressInfo.getQueryInfo()
            inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
            proposer = queryInfo.getProposer()
            startDate = queryInfo.getStartDate()
            patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
            self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)
        else:
            print("pageSum != 0")
            if self.__progressInfo.getPageIndex() != 1:
                self.__query.changePage(self.__progressInfo.getPageIndex())
            else:
                self.__pageCollection.startCollecting(self.__progressInfo.getPatentTypeIndex(),
                                                      self.__progressInfo.getItemIndex())

        print("queryTargetSuccessfully函数end, pageSum = {0}".format(pageSum))


    def queryTargetUnsuccessfully(self):
        print("检索失败")
        self.__connection.refreshUrl()


    def collectingSuccessfully(self):
        print("收集信息成功")
        pi = self.__progressInfo.getPageIndex()
        pi += 1
        if pi >= self.__progressInfo.getPageSum():
            self.__progressInfo.setPageIndex(1)
            self.__progressInfo.setItemIndex(0)
            pt = self.__progressInfo.getPatentTypeIndex()
            if pt >= 2:
                pt = 0
                ii = self.__progressInfo.getInventorIndex()
                if ii < len(self.__progressInfo.getQueryInfo().getInventorList()):
                    self.__progressInfo.setInventorIndex(ii + 1)
                    queryInfo = self.__progressInfo.getQueryInfo()
                    inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
                    proposer = queryInfo.getProposer()
                    startDate = queryInfo.getStartDate()
                    patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
                    self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)
                else:
                    print("ii = {0}".format(ii))
                    self.endProgress()
            else:
                pt += 1
                self.__progressInfo.setPatentTypeIndex(pt)
                queryInfo = self.__progressInfo.getQueryInfo()
                inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
                proposer = queryInfo.getProposer()
                startDate = queryInfo.getStartDate()
                patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
                self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)
        else:
            print("pageIndex = {0}".format(pi))
            self.__progressInfo.setPageIndex(pi)
            self.__progressInfo.setItemIndex(0)
            self.__query.changePage(pi)


    def collectingUnsuccessfully(self, itemIndex):
        print("收集信息失败")
        # TODO:这里某些响应没做好
        self.__progressInfo.setItemIndex(itemIndex)
        queryInfo = self.__progressInfo.getQueryInfo()
        inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
        proposer = queryInfo.getProposer()
        startDate = queryInfo.getStartDate()
        patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
        self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)


    def changePageSuccessfully(self):
        print("换页成功")
        time.sleep(2)
        self.__pageCollection.startCollecting(self.__progressInfo.getPatentTypeIndex())


    def changePageUnsuccessfully(self):
        print("换页失败")
        queryInfo = self.__progressInfo.getQueryInfo()
        inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
        proposer = queryInfo.getProposer()
        startDate = queryInfo.getStartDate()
        patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
        self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)


    def endProgress(self):
        self.__driver.quit()
