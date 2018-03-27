# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906

查询设置模块

具体查询语法详见: https://github.com/will4906/PatentCrawler/wiki/QueryInfo
"""
from entity.query_item import SipoItem, DateSelect, And, ItemGroup, Or, Not

QUERY_LIST = [
    # SipoItem(ipc_class_number='(A01)')
    # 武大20150101-20150110
    SipoItem(proposer='武汉大学', request_date=DateSelect(":", '2015-01-01', '2015-01-10')),
    # SipoItem(abstract='人工智能'),
]


