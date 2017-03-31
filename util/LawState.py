# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
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
        self.driver.execute_script(
            "document.getElementsByClassName(\"item-footer\").item(" + str(which_item) + ").childNodes.item(1).childNodes.item(3).click();"
        )
        return

    # 等待法律信息框加载完成
    def __wait_for_law_state(self):
        if not self.wait_state.wait_for_loading():
            print("等待加载")
            self.__itemCollection.collectingLawDataUnsuccessfully()

        if self.__wait_for_close_button():
            pass
        else:
            print("关闭按钮没出来")
            self.__itemCollection.collectingLawDataUnsuccessfully()

        if self.wait_state.query_result_state():
            pass
        else:
            print("加载异常")
            self.__itemCollection.collectingLawDataUnsuccessfully()# TODO:添加加载失败的处理函数
        return

    def __wait_for_law_state_loading(self):
        if not self.wait_state.wait_for_loading():
            print("等待加载")
            return False
            # self.__itemCollection.collectingLawDataUnsuccessfully()
        return True

    def __check_for_colse_button(self):
        if self.__wait_for_close_button():
            pass
        else:
            print("关闭按钮没出来")
            self.__itemCollection.collectingLawDataUnsuccessfully()

    def __check_if_lost(self):
        if self.wait_state.query_result_state():
            pass
        else:
            print("加载异常")
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

    # 采集法律信息数据
    def collecting_law_state(self, which_item):
        try:
            print("点击按钮")
            WaitEngine.waitForSeconds(2)
            self.__click_law_state_button(which_item)
            if self.__wait_for_law_state_loading() is True:
                self.__check_for_colse_button()
                self.__check_if_lost()
            else:
                print("点击按钮")
                WaitEngine.waitForSeconds(2)
                self.__click_law_state_button(which_item)
                if self.__wait_for_law_state_loading() is True:
                    self.__check_for_colse_button()
                    self.__check_if_lost()
                else:
                    self.__itemCollection.collectingLawDataUnsuccessfully()
                    return
            print("法律状态")
            law_state = self.__get_law_state()
            if law_state.find("无数据") == -1:
                print("法律日期")
                law_update = self.__get_law_update()
            else:
                law_update = "无数据"
            print("关闭按钮")
            self.__close_law_state()
            print("采集成功")
            self.__itemCollection.collectingLawDataSuccessfully(law_update, law_state)
        except Exception as e:
            print("采集异常")
            print(e)
            self.__itemCollection.collectingLawDataUnsuccessfully()
        return

