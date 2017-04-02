# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from enums.Config import Config


class Connection:
    def __init__(self, progressController):
        self.__progressController = progressController
        # self.__url = "http://www.baidu.com/"
        self.__url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml"
        self.__driver = progressController.getWebDriver()

    def connectUrl(self):
        try:
            self.__driver.get(self.__url)
            self.__progressController.loadUrlSuccessfully()
            return True
        except Exception as e:
            Config.writeException(e)
            self.__progressController.loadUrlUnsuccessfully()
            return False

    def refreshUrl(self):
        try:
            self.__driver.refresh()
            self.__progressController.loadUrlSuccessfully()
            return True
        except Exception as e:
            Config.writeException(e)
            self.__progressController.loadUrlUnsuccessfully()
            return False