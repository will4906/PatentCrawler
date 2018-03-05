# -*- coding: utf-8 -*-
"""
Created on 2018/2/27

@author: will4906
"""
from entity.query_item import title_define


def resolve_data(item, title, itemvalue):
    for key, value in title_define.items():
        if title.find(value) != -1:
            item[key] = itemvalue
            break
