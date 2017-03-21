# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def connect_url(driver, url):
    driver.get(url)
    print("已连接")
    return


def input_parameter(driver, inventor_text, proposer_text, time_text):
    search_button_xpath = "/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]"
    inventor_input_id = "tableSearchItemIdIVDB021"
    proposer_input_id = "tableSearchItemIdIVDB020"
    time_select_id = "IVDB007select"
    time_input_id = "tableSearchItemIdIVDB007"

    load_index_ok = False
    while load_index_ok is False:
        try:
            search_button = driver.find_element_by_xpath(search_button_xpath)
            inventor_input = driver.find_element_by_id(inventor_input_id)
            proposer_input = driver.find_element_by_id(proposer_input_id)
            time_select = driver.find_element_by_id(time_select_id)
            time_input = driver.find_element_by_id(time_input_id)

            load_index_ok = True

            if search_button.is_displayed() and inventor_input.is_displayed() and proposer_input.is_displayed() and time_select.is_displayed() and time_input.is_displayed():
                # 填写发明人
                driver.execute_script(
                    "document.getElementById(\"" + inventor_input_id + "\").setAttribute(\"value\",\"" + inventor_text + "\")")
                # 填写申请人
                driver.execute_script(
                    "document.getElementById(\"" + proposer_input_id + "\").setAttribute(\"value\",\"" + proposer_text + "\")")
                # 点击时间的check_list
                driver.execute_script(
                    "document.getElementById(\"" + time_select_id + "\").firstElementChild.firstElementChild.click();")
                time.sleep(2)
                driver.execute_script(
                    "document.getElementById(\"" + time_select_id + "\").firstElementChild.childNodes[2].childNodes[2].firstElementChild.click();")
                # 填写时间
                driver.execute_script(
                    "document.getElementById(\"" + time_input_id + "\").setAttribute(\"value\",\"" + time_text + "\")")
                time.sleep(3)
                # 点击检索按钮
                search_button.click()
                print("开始检索")
            else:
                print("按钮没显示")

        except Exception as e:
            print(e)
            load_index_ok = False
            driver.refresh()
            time.sleep(3)


def check_for_loading():
    fail_str = "数据正在加载中"

    bs_object = BeautifulSoup(driver.page_source, "html.parser")
    load_success = bs_object.prettify().find(fail_str)
    print(fail_str)
    while load_success is not -1:
        bs_object = BeautifulSoup(driver.page_source, "html.parser")
        load_success = bs_object.prettify().find(fail_str)

    print("加载完成")

    return bs_object

if __name__ == '__main__':

    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    connect_url(driver, "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml")
    input_parameter(driver, "陈思平", "深圳大学", "2001-01-01")

    strLeft = "/div[4]/div[1]/ul/li["
    strRight = "]/div/div[1]/h1/div[2]/a/b"

    bsObject = check_for_loading()

    name = driver.execute_script(
        "return document.getElementsByName(\"titleHidden\").item(0).attributes.getNamedItem(\"value\").textContent;")
    print(name)
    # searchResult = bsObject.find(class_ = "list-container")
    # print(searchResult)
    #
    # searchResultBs = BeautifulSoup(str(searchResult), "html.parser")
    # print(searchResultBs)

    driver.close()
    # contentList = bsObject.find_all(class_ = "item")
    # print(bsObject.prettify())
    # for index in range(0, len(contentList)):
    #     print(contentList[index].find('b').get_text())
        # title = searchResult.find_element_by_xpath(strLeft + str(index) + strRight)
        # driver.implicitly_wait(20)
        # print(title.getText())

    # print(driver.page_source)
    # bsObject = BeautifulSoup(driver.page_source,"html.parser")
    # # contentList = bsObject.find_all(class_ = "item-content-body")
    # # print(len(contentList))
    # # for i in range(len(contentList)):
    # #     print(contentList[i].get_text())
    # searchResultDiv = bsObject.find(id="search-result")
    # driver.implicitly_wait(20)
    # if searchResultDiv is not None:
    #     print(searchResultDiv.get_text())


#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div/div[1]
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div/div[1]/h1
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div/div[1]/h1/div[2]
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div/div[1]/h1/div[2]/a
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[1]/div/div[1]/h1/div[2]/a/b


#     //*[@id="search_result"]/div[4]/div[1]/ul/li[3]/div/div[1]/h1/div[2]/a/b
#     数据正在加载中
#     //*[@id="search_result"]/div[4]/div[1]/ul/li[4]/div/div[1]/h1/div[2]/a/b

# #search_result > div.re-content.search-mode-content > div.list-container > ul > li:nth-child(1) > div > div.item-header.clear > h1 > div:nth-child(2) > a > b
# <b style="color: #4B4B4B">一种超声探头以及超声成像辅助诊断系统</b>
# //*[@id="search_result"]/div[4]/div[1]