# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import requests
from bs4 import BeautifulSoup

from service.CookieService import CookieService
from service.LoginService import LoginService

if __name__ == '__main__':
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://www.pss-system.gov.cn",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/preExecuteSearch!preExecuteSearch.do"
    resp = requests.get(url, headers=headers)
    print(resp.content)
    LoginService(resp.cookies).startLogin()

    url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0712AC!executeCommandSearchUnLogin.do"
    formData = {
        "searchCondition.searchExp": '?发明人=(陈思平)',
        "searchCondition.dbId": "VDB",
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.extendInfo['MODE']": "MODE_TABLE",
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        "searchCondition.originalLanguage": "",
        "searchCondition.targetLanguage": "",
        "wee.bizlog.modulelevel": "0200201",
        "resultPagination.limit": 80
    }
    resp = requests.post(url, data=formData, headers=headers)
    soup = BeautifulSoup(resp.content, "html5lib")
    pageTop = soup.find(attrs={"class": "page_top"})
    strSum = pageTop.get_text(strip=True)
    patentSum = int(strSum[strSum[2:].find("页") + 3:strSum.find("条")])





























