# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from util.WaitEngine import WaitEngine


class LawState:
    close_btn_string = "取消"

    def __init__(self, driver):
        self.wait_state = WaitEngine(driver)
        self.driver = driver

    # 点击法律信息的按钮
    def __click_law_state_button(self, which_item):
        # 法律信息
        self.driver.execute_script(
            "document.getElementsByClassName(\"item-footer\").item(" + str(which_item) + ").childNodes.item(1).childNodes.item(3).click();"
        )
        return

    # 等待法律信息框加载完成
    def __wait_for_law_state(self):
        self.wait_state.wait_for_loading()
        self.__wait_for_close_button()
        if self.wait_state.query_result_state():
            pass    # TODO:添加加载失败的处理函数
        else:
            pass

        return

    # 等待关闭框加载完成
    def __wait_for_close_button(self):
        while self.driver.page_source.find(self.close_btn_string) is -1:
            pass
        return

    # 采集日期最近的法律信息
    def __get_law_state(self):
        return self.driver.execute_script(
            "return document.getElementById(\"lawResult\").getElementsByTagName(\"td\").item(document.getElementById(\"lawResult\").getElementsByTagName(\"td\").length - 1).innerText;"
        )

    # 关闭法律信息框
    def __close_law_state(self):
        self.driver.execute_script(
            "document.getElementsByClassName(\"ui-dialog-close\").item(0).click();"
        )
        return

    # 采集法律信息数据
    def collecting_law_state(self, which_item):
        self.__click_law_state_button(which_item)
        self.__wait_for_law_state()
        law_state = self.__get_law_state()
        self.__close_law_state()
        return law_state

