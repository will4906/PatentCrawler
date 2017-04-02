# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from enums.Config import Config
from util.WaitEngine import WaitEngine


class LawState:
    close_btn_string = "取消"

    def __init__(self, driver, itemCollection):
        self.wait_state = WaitEngine(driver)
        self.driver = driver
        self.__itemCollection = itemCollection

    # 点击法律信息的按钮
    def __click_law_state_button(self, which_item):
        # 法律信息
        try:
            self.driver.execute_script(
                "document.getElementsByClassName(\"item-footer\").item(" + str(which_item) + ").childNodes.item(1).childNodes.item(3).click();"
            )
        except Exception as e:
            Config.writeException(e)
            print(e)
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName(\"item-footer\").item(" + str(
                        which_item) + ").childNodes.item(1).childNodes.item(3).click();"
                )
            except Exception as e:
                print(e)
                Config.writeException(e)
        return

    # 等待法律信息框加载完成
    def __wait_for_law_state(self):
        if not self.wait_state.wait_for_loading():
            Config.writeLog("等待超时")
            print("等待超时")
            self.__itemCollection.collectingLawDataUnsuccessfully()

        if self.__wait_for_close_button():
            pass
        else:
            Config.writeLog("关闭按钮没出来")
            print("关闭按钮没出来")
            self.__itemCollection.collectingLawDataUnsuccessfully()

        if self.wait_state.query_result_state():
            pass
        else:
            Config.writeLog("加载异常")
            print("加载异常")
            self.__itemCollection.collectingLawDataUnsuccessfully()# TODO:添加加载失败的处理函数
        return

    def __wait_for_law_state_loading(self):
        if not self.wait_state.wait_for_loading():
            Config.writeLog("等待超时")
            print("等待超时")
            return False
            # self.__itemCollection.collectingLawDataUnsuccessfully()
        return True

    def __check_for_colse_button(self):
        if self.__wait_for_close_button():
            pass
        else:
            Config.writeLog("关闭按钮没出来")
            self.__itemCollection.collectingLawDataUnsuccessfully()

    def __check_if_lost(self):
        if self.wait_state.query_result_state():
            pass
        else:
            print("加载异常")
            Config.writeLog("加载异常")
            self.__itemCollection.collectingLawDataUnsuccessfully()# TODO:添加加载失败的处理函数

    # 等待关闭按钮加载完成
    def __wait_for_close_button(self):
        key = WaitEngine.generateOverTimeKey()
        while self.driver.page_source.find(self.close_btn_string) is -1:
            if WaitEngine.isOverTime(key, 2):
                return False
        return True

    # 采集日期最近的法律信息
    def __get_law_state(self):
        return self.driver.execute_script(
            "return document.getElementById(\"lawResult\").getElementsByTagName(\"td\").item(document.getElementById(\"lawResult\").getElementsByTagName(\"td\").length - 1).innerText;"
        )

    def __get_law_update(self):
        law_update = self.driver.execute_script(
            "return document.getElementById(\"lawResult\").children[1].children[document.getElementById(\"lawResult\").children[1].children.length-1].children[1].innerText;"
        )
        return law_update
    # 关闭法律信息框
    def __close_law_state(self):
        self.driver.execute_script(
            "document.getElementsByClassName(\"ui-dialog-close\").item(0).click();"
        )
        return

    def __hasLawItem(self):
        len = self.driver.execute_script(
            "return document.getElementById(\"lawResult\").getElementsByTagName(\"td\").length;"
        )
        if len > 0:
            return True
        else:
            return False

    def hasShowLawStateDialog(self):
        try:
            length = self.driver.execute_script(
                "return document.getElementsByClassName(\"ui-dialog\").length;"
            )
            if length > 0:
                return True
            else:
                return False
        except:
            return False

    def waitForLawStateDialog(self, whichItem):
        tryTimes = 0
        while not self.hasShowLawStateDialog():
            WaitEngine.waitForSeconds(2)
            self.__click_law_state_button(whichItem)
            tryTimes += 1
            if tryTimes > 3:
                break
        if tryTimes >= 4:
            return False
        else:
            return True

    def collectingLawState(self, whichItem):
        try:
            Config.writeLog("点击按钮")
            WaitEngine.waitForSeconds(1)
            self.__click_law_state_button(whichItem)
            WaitEngine.waitForSeconds(2)
            if self.waitForLawStateDialog(whichItem):
                if self.__wait_for_law_state_loading() is True:
                    self.__check_for_colse_button()
                    self.__check_if_lost()
                else:
                    self.__itemCollection.collectingLawDataUnsuccessfully()
                    return
            else:
                self.__itemCollection.collectingLawDataUnsuccessfully()
                return
            Config.writeLog("法律状态")
            law_state = self.__get_law_state()
            if law_state.find("无数据") == -1:
                Config.writeLog("法律日期")
                law_update = self.__get_law_update()
            else:
                law_update = "无数据"
            Config.writeLog("关闭按钮")
            self.__close_law_state()
            Config.writeLog("采集成功")
            self.__itemCollection.collectingLawDataSuccessfully(law_update, law_state)
        except Exception as e:
            print("采集异常")
            Config.writeLog("采集异常")
            Config.writeException(e)
            self.__itemCollection.collectingLawDataUnsuccessfully()

    #     TODO:处理点击失败的响应

    # 采集法律信息数据
    def collecting_law_state(self, which_item):
        try:
            Config.writeLog("点击按钮")
            WaitEngine.waitForSeconds(2)
            self.__click_law_state_button(which_item)
            if self.__wait_for_law_state_loading() is True:
                self.__check_for_colse_button()
                self.__check_if_lost()
            else:
                Config.writeLog("点击按钮")
                WaitEngine.waitForSeconds(2)
                self.__click_law_state_button(which_item)
                if self.__wait_for_law_state_loading() is True:
                    self.__check_for_colse_button()
                    self.__check_if_lost()
                else:
                    self.__itemCollection.collectingLawDataUnsuccessfully()
                    return
            Config.writeLog("法律状态")
            law_state = self.__get_law_state()
            if law_state.find("无数据") == -1:
                Config.writeLog("法律日期")
                law_update = self.__get_law_update()
            else:
                law_update = "无数据"
            Config.writeLog("关闭按钮")
            self.__close_law_state()
            Config.writeLog("采集成功")
            self.__itemCollection.collectingLawDataSuccessfully(law_update, law_state)
        except Exception as e:
            print("采集异常")
            Config.writeLog("采集异常")
            Config.writeException(e)
            self.__itemCollection.collectingLawDataUnsuccessfully()
        return

