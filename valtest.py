# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from entity.QueryItem import QueryItem, DateSelect


if __name__ == '__main__':
    q = QueryItem(inventorName=["陈思平", "陈昕"],
                  publishDate=DateSelect(select='>=', date='2025-07-08'),
                  proposerName=['深圳大学','北京科技大学'],
                  inventionType=['I', 'U', 'Y'],
                  publishCountry=['cn','us'])
    # q.generateSearchExp()
    # for t in q.searchExpList:
    #     print(t)
    q.createTarget()
    for t in q.targetList:
        print(t.publishDate, t.proposerName, t.inventorName + t.inventionType + str(t.publishCountry))


