# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import xlwt
import xlrd


def init_excel_config(date):
    title_list = ["专利类型", "专利名称", "法律状态", "申请公布日/授权公告日", "申请号", "申请日", "申请人/专利权人", "发明人"]
    work_book = xlwt.Workbook()
    work_sheet = work_book.add_sheet("Sheet1")
    for index, each in enumerate(title_list):
        work_sheet.write(0, index, each)
    work_book.save("专利({0}).xls".format(date))
    return work_book, work_sheet


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

    check_for_loading()

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


def wait_for_lawstate(driver):
    fail_str = "数据正在加载中"
    close_btn_string = "取消"

    while BeautifulSoup(driver.page_source, "html.parser").prettify().find(fail_str) is not -1:
        # print("点击法律信息，等待数据加载")
        pass
    while BeautifulSoup(driver.page_source, "html.parser").prettify().find(close_btn_string) is -1:
        # print("点击法律信息，等待取消按钮")
        pass


def collecting_data(driver):
    itemLength = driver.execute_script("return document.getElementsByClassName(\"item\").length;")

    for i in range(itemLength):
        is_normal_data = False

        try:
            # 专利名称
            name = driver.execute_script(
                "return document.getElementsByName(\"titleHidden\").item(" + str(
                    i) + ").attributes.getNamedItem(\"value\").textContent;")
            if name != "":
                is_normal_data = True
            # 专利类型
            type = driver.execute_script(
                "return document.getElementsByClassName(\"item-header\").item(" + str(
                    i) + ").childNodes.item(3).childNodes.item(3).textContent;")
        except:
            is_normal_data = False

        if is_normal_data is True:
            # 申请号
            driver.execute_script(
                "document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(1).removeChild(document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(1).childNodes.item(0));"
            )
            requestNumber = driver.execute_script(
                "return document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(1).childNodes.item(0).textContent;"
            )
            # 申请日
            driver.execute_script(
                "document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(3).removeChild(document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(3).childNodes.item(0));"
            )
            requestDate = driver.execute_script(
                "return document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(3).childNodes.item(1).textContent;"
            )
            # 公布日
            driver.execute_script(
                "document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(7).removeChild(document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(7).childNodes.item(0));"
            )
            announcement_date = driver.execute_script(
                "return document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(7).childNodes.item(1).textContent;"
            )
            # 申请人
            propsorName = driver.execute_script(
                "return document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(11).innerText;"
            )
            inventorName = driver.execute_script(
                "return document.getElementsByClassName(\"item-content-body\").item(" + str(
                    i) + ").childNodes.item(13).innerText;"
            )
            # 法律信息
            driver.execute_script(
                "document.getElementsByClassName(\"item-footer\").item(" + str(
                    i) + ").childNodes.item(1).childNodes.item(3).click();"
            )
            wait_for_lawstate(driver)
            law_state = driver.execute_script(
                "return document.getElementById(\"lawResult\").getElementsByTagName(\"td\").item(document.getElementById(\"lawResult\").getElementsByTagName(\"td\").length - 1).innerText;"
            )
            driver.execute_script(
                "document.getElementsByClassName(\"ui-dialog-close\").item(0).click();"
            )
            print(name + "\t" + type[1:-1] + "\t" + requestNumber + "\t" + requestDate + "\t" + announcement_date + "\t" + propsorName[10:] + "\t" + inventorName + "\t" + law_state)

    return

if __name__ == '__main__':
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    init_excel_config(date)

    url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml"
    driver = webdriver.PhantomJS(executable_path='.\phantomjs.exe')

    connect_url(driver, url)
    input_parameter(driver, "陈思平", "深圳大学", "2001-01-01")

    bsObject = check_for_loading()
    # TODO: 有可能出现“检索失败”的情况，要进行处理

    collecting_data(driver)

    driver.close()
