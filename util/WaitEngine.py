# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
import time


class WaitEngine:
    query_lost = "检索失败"
    fail_string = "查询出错"
    loading_string = "数据正在加载中"

    def __init__(self, driver):
        self.driver = driver

    # 是否正在加载
    def is_loading(self):
        if self.driver.page_source.find(self.loading_string) == -1:
            return False
        else:
            return True

    @staticmethod
    def waitForSeconds(second=2):
        time.sleep(second)

    @staticmethod
    def generateOverTimeKey():
        return time.time()

    @staticmethod
    def isOverTime(key, minute=1):
        t = time.time()
        if (t - key) >= (minute * 60):
            return True
        else:
            return False

    # 等待加载
    # 返回值：True没有超时，False超时
    def wait_for_loading(self):
        key = WaitEngine.generateOverTimeKey()
        while self.is_loading():
            if WaitEngine.isOverTime(key, 2):
                return False
        return True

    # 查询状态结果，True则查询有结果，False则查询失败
    def query_result_state(self):
        if self.driver.page_source.find(self.fail_string) == -1:
            if self.driver.page_source.find(self.query_lost) == -1:
                return True
            else:
                return False
        else:
            return False
