# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import json
from copy import deepcopy

import requests

from entity.QueryItem import QueryItem, DateSelect, And, ItemGroup, Or, Not

if __name__ == '__main__':
    inventorList = [ItemGroup(And("陈思平", "董磊")), "陈昕", "汪天富", "谭力海", "彭珏", "但果", "叶继伦", "覃正笛",
                    "张旭", "张会生", "钱建庭", "丁惠君", "刁现芬", "沈圆圆", "周永进", "孔湉湉",
                    "陆敏华", "张新宇", "孙怡雯", "李乔亮", "齐素文", "徐海华", "倪东", "刘维湘",
                    "李抱朴", "黄炳升", "徐敏", "雷柏英", "胡亚欣", "何前军", "郑介志", "常春起",
                    "陈雯雯", "罗永祥", "黄鹏", "林静", "王倪传", "刘立", "张治国", "董磊"]
    infoList = []
    for i in inventorList:
        queryItem = QueryItem(proposer_people='深圳大学',
                          inventor_people=i,
                          request_date=DateSelect('>=', '2001-01-01'),
                              invention_type=Or('I', 'U'),
                              publish_country=ItemGroup(Or=Or('HK')))
        infoList.append(deepcopy(queryItem))
    for i in infoList:
        print(i.__getattribute__('search_exp'))

