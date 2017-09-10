# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import json

import requests

from entity.QueryItem import QueryItem, DateSelect, And, ItemGroup, Or, Not

if __name__ == '__main__':
    queryItem = QueryItem(proposer_people=ItemGroup(And=And('深圳大学')),
                          inventor_people='陈思平',
                          request_date=DateSelect('>=', '2001-01-01'))
    print(queryItem.__getattribute__('search_exp'))

