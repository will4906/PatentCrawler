# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
import os

import time
import os

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from entity.ProgressInfo import ProgressInfo
from enums.Config import Config
from service.Connection import Connection
from service.PageCollection import PageCollection
from service.Query import Query
from selenium import webdriver


class ProgressController:
    def __init__(self, browser):
        self.__browser = browser
        self.__driver = self.__generateWebDriver(browser)
        self.__connection = Connection(self)
        self.__query = Query(self)
        self.__progressInfo = ProgressInfo()
        self.__pageCollection = PageCollection(self, self.__progressInfo.getCollectionResult())
        self.__refreshLostTime = 0
        self.__rConnectLostTime = 0
        return

    def __generateWebDriver(self, browser):
        driver = None
        if isinstance(browser, str):
            if browser.upper() == "CHROME":
                driver = webdriver.Chrome()
                driver.set_page_load_timeout(120)
            elif browser.upper() == "PHANTOMJS":
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = (
                    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
                )
                # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"
                # dcap["phantomjs.page.settings.userAgent"] = (
                #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"
                # )
                driver = webdriver.PhantomJS(executable_path='.\\res\phantomjs.exe', desired_capabilities=dcap)
                driver.set_page_load_timeout(120)
            elif browser.upper() == "FIREFOX":
                binary = FirefoxBinary(r'C:\Software\MozillaFirefox\firefox.exe')
                driver = webdriver.Firefox(firefox_binary=binary)
        else:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
            )
            driver = webdriver.PhantomJS(executable_path='.\\res\phantomjs.exe', desired_capabilities=dcap)
            driver.set_page_load_timeout(120)
        return driver

    def getWebDriver(self):
        return self.__driver

    def startProgress(self):
        print("开始爬取进程")
        try:
            self.__connection.connectUrl()
        except Exception as e:
            print(e)

    def loadUrlSuccessfully(self):
        print("成功连接url")
        if self.__driver.page_source.find("您的操作太过频繁") != -1:
            print(Config.REJECT_WAY)
            self.endProgress()
            return
        self.__refreshLostTime = 1
        self.__rConnectLostTime = 1
        queryInfo = self.__progressInfo.getQueryInfo()
        inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
        proposer = queryInfo.getProposer()
        startDate = queryInfo.getStartDate()
        patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
        self.__query.queryTarget(inventor, proposer, startDate, patentTypeIndex)

    def loadUrlUnsuccessfully(self):
        print("url连接失败")
        self.__refreshLostTime += 1
        if self.__refreshLostTime % 5 == 0:
            self.__rConnectLostTime += 1
            if self.__rConnectLostTime % 2 == 0:
                self.__driver.quit()
                time.sleep(10)
                self.__driver = self.__generateWebDriver(self.__browser)
            self.__connection.connectUrl()
        else:
            self.__connection.refreshUrl()

    def queryTargetSuccessfully(self, pageSum):
        print("检索成功")
        self.__refreshLostTime = 1
        self.__rConnectLostTime = 1
        self.__progressInfo.setPageSum(pageSum)

        if pageSum == 0:
            print("pageSum = 0")
            self.__progressInfo.setItemIndex(0)
            self.__progressInfo.setPageIndex(1)
            pt = self.__progressInfo.getPatentTypeIndex()
            if pt >= 2:
                print("pt >= 2")
                self.__progressInfo.setPatentTypeIndex(0)
                inventorIndex = self.__progressInfo.getInventorIndex() + 1
                if inventorIndex >= len(self.__progressInfo.getQueryInfo().getInventorList()):
                    self.endProgress()
                else:
                    self.__progressInfo.setInventorIndex(inventorIndex)
                    queryInfo = self.__progressInfo.getQueryInfo()
                    print(queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()])
            else:
                print("pt < 2")
                self.__progressInfo.setPatentTypeIndex(pt + 1)

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
        self.__refreshLostTime += 1
        if self.__refreshLostTime % 5 == 0:
            self.__rConnectLostTime += 1
            if self.__rConnectLostTime % 2 == 0:
                self.__driver.quit()
                time.sleep(10)
                self.__driver = self.__generateWebDriver(self.__browser)
            self.__connection.connectUrl()
        else:
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
                if ii < len(self.__progressInfo.getQueryInfo().getInventorList()) - 1:
                    self.__progressInfo.setInventorIndex(ii + 1)
                    queryInfo = self.__progressInfo.getQueryInfo()
                    inventor = queryInfo.getInventorList()[self.__progressInfo.getInventorIndex()]
                    proposer = queryInfo.getProposer()
                    startDate = queryInfo.getStartDate()
                    patentTypeIndex = self.__progressInfo.getPatentTypeIndex()
                    print(inventor)
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
        time.sleep(3)
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
        print("结束进程")
        self.__driver.quit()
        time.sleep(1)
        os._exit(0)
