# -*- coding: utf-8 -*-
"""
Created on 2017/5/11

@author: will4906
"""
import requests
import time

from bs4 import BeautifulSoup

from util.HeadersEngine import HeadersEngine

def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

#  一种超声粘弹性测量方法及系统
# 【公开】
# 发明申请
# 申请号­ :CN201610334175.5
# 申请日 :2016.05.19
# 公开（公告）号­ :CN106037816A
# 公开（公告）日 :2016.10.26
# IPC分类号 :A61B8/08;
# 申请（专利权）人 :深圳大学;
# 发明人 :刁现芬;朱菁;覃正笛;陈思平;
# 代理人 :王永文;刘文求;
# 代理机构 :深圳市君胜知识产权代理事务所 44268;深圳市君胜知识产权代理事务所 44268;
# 外观设计洛迦诺分类号 :24-01(10)
# 实质审查的生效
# 20161123
# 公开（公告）日>=2001-01-01 AND 申请（专利权）人=(深圳大学) AND 发明人=(陈思平) AND 发明类型=("I") AND 公开国=(HK OR MO OR TW OR CN)
# VDB:((PD>='2001-01-01' AND PAVIEW='深圳大学' AND INVIEW='陈思平' AND DOC_TYPE='I' AND (CC='HK' OR CC='MO' OR CC='TW' OR CC='CN')))
if __name__ == '__main__':
    formData = {
        "resultPagination.limit" : "80",
        "resultPagination.start": "12",
        "resultPagination.totalCount": "91",
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.dbId": "",
        "searchCondition.power": "false",
        "searchCondition.searchExp": "公开（公告）日>=2001-01-01 AND 申请（专利权）人=(深圳大学) AND 发明人=(陈思平)",
        "searchCondition.executableSearchExp": "VDB:((PD>='2001-01-01' AND PAVIEW='深圳大学' AND INVIEW='陈思平'))"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": HeadersEngine().getRandomUserAgent()
    }
    r = requests.post(
        url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml",
        headers=headers,
        data=formData
    )
    soup = BeautifulSoup(r.text, "lxml")
    itemList = soup.find_all(attrs={"class": "item"})
    for item in itemList:
        itemSoup = BeautifulSoup(item.prettify(), "lxml")
        header = itemSoup.find(attrs={"class": "item-header"})
        print(header.find("h1").get_text(strip=True))
        print(header.find(attrs={"class": "btn-group left clear"}).get_text(strip=True))
        content = itemSoup.find(attrs={"class": "item-content-body left"})
        contentList = content.find_all("p")
        for c in contentList:
            print(c.get_text(strip=True))
