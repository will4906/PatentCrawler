# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time

if __name__ == '__main__':

    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')
    driver.get("http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml")
    print("已连接")
    searchButton = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]")
    inventorInput = driver.find_element_by_id("tableSearchItemIdIVDB021")
    if searchButton.is_displayed() is True and inventorInput.is_displayed():
        driver.execute_script("document.getElementById(\"tableSearchItemIdIVDB021\").setAttribute(\"value\",\"陈思平\")")
        # driver.execute_script("document.getElementById(\"tableSearchItemIdIVDB020\").setAttribute(\"value\",\"深圳大学\")")
        time.sleep(3)
        searchButton.click()
        print("按钮已点击")
    else:
        print("按钮没显示")

    strLeft = "/div[4]/div[1]/ul/li["
    strRight = "]/div/div[1]/h1/div[2]/a/b"

    failStr = "数据正在加载中"

    bsObject = BeautifulSoup(driver.page_source, "html.parser")
    loadSuccess = bsObject.prettify().find(failStr)
    while loadSuccess is not -1:
        bsObject = BeautifulSoup(driver.page_source, "html.parser")
        loadSuccess = bsObject.prettify().find(failStr)
        print("还没加载完")
    print("加载完成")
    # bsObject.find()
    # searchResult = driver.find_element_by_id('search_result')
    contentList = bsObject.find_all(class_ = "item")
    print(bsObject.prettify())
    for index in range(0, len(contentList)):
        print(contentList[index].find('b').get_text())
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
    driver.close()

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