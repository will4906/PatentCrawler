# -*- coding: utf-8 -*-
"""
Created on 2017/5/11

@author: will4906
"""
import requests

from util.HeadersEngine import HeadersEngine

if __name__ == '__main__':
    # r = requests.post("http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/biaogejsAC!executeCommandSearchUnLogin.do", data={
    #     "searchCondition.searchExp": "公开（公告）日>=2001-01-01 AND 申请（专利权）人=(深圳大学) AND 发明人=(陈思平) AND 发明类型=(\"I\") AND 公开国=(HK OR CN) ",
    #     "searchCondition.dbId": "VDB",
    #     "searchCondition.searchType": "Sino_foreign",
    #     "searchCondition.power": "false",
    #     "wee.bizlog.modulelevel": "0200201",
    #     "resultPagination.limit": "12"
    # })
    # print(r.text)
    h = HeadersEngine()
    print(h.getUserAgent())