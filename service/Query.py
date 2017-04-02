# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from enums.Config import Config
from util.WaitEngine import WaitEngine


class Query:
    search_button_xpath = "/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]"
    inventor_input_id = "tableSearchItemIdIVDB021"
    proposer_input_id = "tableSearchItemIdIVDB020"
    time_select_id = "IVDB012select"
    time_input_id = "tableSearchItemIdIVDB012"

    def __init__(self, progressController):
        self.__progressController = progressController
        self.__driver = progressController.getWebDriver()
        self.__waitEngine = WaitEngine(self.__driver)

    def queryTarget(self, inventor, proposer, startDate, patentTypeIndex):
        if self.__waitEngine.wait_for_loading():
            if self.__isElementLoadingSuccess():
                if self.__inputQueryTargetData(inventor, proposer, startDate, patentTypeIndex):
                    if self.__waitEngine.wait_for_loading():
                        pageSum = self.__getPageSum()
                        if pageSum is not None:
                            self.__progressController.queryTargetSuccessfully(pageSum)
                            return True
                        else:
                            print("页码为零")
                            Config.writeLog("页码为零")
                            self.__progressController.queryTargetUnsuccessfully()
                            return False
                    else:
                        print("查询等待超时")
                        Config.writeLog("查询等待超时")
                        self.__progressController.queryTargetUnsuccessfully()
                        return False
                else:
                    print("查询失败")
                    Config.writeLog("查询失败")
                    self.__progressController.queryTargetUnsuccessfully()
                    return False
            else:
                print("元素未加载")
                Config.writeLog("元素未加载")
                self.__progressController.queryTargetUnsuccessfully()
                return False
        else:
            print("url加载超时")
            Config.writeLog("url加载超时")
            self.__progressController.queryTargetUnsuccessfully()
            return False

    # 元素是否加载完成
    def __isElementLoadingSuccess(self):
        try:
            search_button = self.__driver.find_element_by_xpath(Query.search_button_xpath)
            inventor_input = self.__driver.find_element_by_id(Query.inventor_input_id)
            proposer_input = self.__driver.find_element_by_id(Query.proposer_input_id)
            time_select = self.__driver.find_element_by_id(Query.time_select_id)
            time_input = self.__driver.find_element_by_id(Query.time_input_id)

            if search_button.is_displayed() and inventor_input.is_displayed() and proposer_input.is_displayed() and time_select.is_displayed() and time_input.is_displayed():
                return True
            else:
                print("元素没显示")
                Config.writeLog("元素没显示")
                return False
        except Exception as e:
            print("元素抛异常")
            Config.writeLog("元素抛异常")
            Config.writeException(e)
            return False

    def __inputQueryTargetData(self, inventor, proposer, startDate, patentTypeIndex):
        try:
            # 填写发明人
            self.__driver.execute_script(
                "document.getElementById(\"" + Query.inventor_input_id + "\").setAttribute(\"value\",\"" + inventor + "\")")
            Config.writeLog("发明人")
            # 填写申请人
            self.__driver.execute_script(
                "document.getElementById(\"" + Query.proposer_input_id + "\").setAttribute(\"value\",\"" + proposer + "\")")
            Config.writeLog("申请人")
            # 点击时间的check_list
            self.__driver.execute_script(
                "document.getElementById(\"" + Query.time_select_id + "\").firstElementChild.firstElementChild.click();")
            WaitEngine.waitForSeconds(2)        # 等待两秒
            self.__driver.execute_script(
                "document.getElementById(\"" + Query.time_select_id + "\").firstElementChild.childNodes[2].childNodes[2].firstElementChild.click();")
            Config.writeLog("点击时间")
            # 填写时间
            self.__driver.execute_script(
                "document.getElementById(\"" + Query.time_input_id + "\").setAttribute(\"value\",\"" + startDate + "\")")
            Config.writeLog("填写时间")
            # 选择专利类型
            self.__choosePatentType(patentTypeIndex)
            Config.writeLog("专利类型")
            WaitEngine.waitForSeconds(3)        # 等待三秒
            # 点击检索按钮
            self.__driver.execute_script(
                "document.getElementsByClassName(\"box-content-bottom\").item(0).childNodes.item(5).click();"
            )
            Config.writeLog("点击按钮")
            return True
        except Exception as e:
            Config.writeException(e)
            print(e)
            return False

    # 选择专利类型
    def __choosePatentType(self, patentTypeIndex):
        for i in range(3):                  # 去掉多余的active
            self.__driver.execute_script(
                "document.getElementsByName(\"inventiontype\").item(" + str(i) + ").classList.remove(\"active\");"
            )
        self.__driver.execute_script(
            "document.getElementsByName(\"inventiontype\").item(" + str(patentTypeIndex) + ").classList.add(\"active\");"
        )

    # 获取页码总数
    def __getPageSum(self):
        if self.__driver.page_source.find("没有检索到") != -1:
            return 0
        else:
            try:
                page_sum_str = self.__driver.execute_script(
                    "return document.getElementsByClassName(\"page_top\").item(0).childNodes.item(document.getElementsByClassName(\"page_top\").item(0).childNodes.length - 1).textContent;"
                )
                strTemp = page_sum_str[page_sum_str.find("共") + 1:-1]
                page_sum = int(strTemp[:strTemp.find("页")])
                return page_sum
            except Exception as e:
                Config.writeException(e)
                print(e)
                return None


    def changePage(self, pageIndex):
        try:
            self.__driver.execute_script(
                "document.getElementById(\"txt\").setAttribute(\"value\", " + str(pageIndex) + ");"
            )
            self.__driver.execute_script(
                "document.getElementsByClassName(\"page_bottom\").item(0).childNodes.item(document.getElementsByClassName(\"page_bottom\").item(0).childNodes.length - 2).click();"
            )
            self.__progressController.changePageSuccessfully()
            return True
        except Exception as e:
            Config.writeException(e)
            print(e)
            self.__progressController.changePageUnsuccessfully()
            return False
