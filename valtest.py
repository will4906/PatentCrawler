# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from entity.QueryItem import QueryItem, DateSelect


if __name__ == '__main__':
    q = QueryItem(requestNumber=['ZL123', '1234'], requestDate=[DateSelect(), DateSelect(date='2017-07-08')], publishDate=[DateSelect(), DateSelect(date='2017-07-08'),DateSelect(date='2025-07-08')])
    q.generateSearchExp()
    for t in q.searchExpList:
        print(t)


