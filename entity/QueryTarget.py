# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""


class QueryTarget:
    def __init__(self, requestNumber=None, requestDate=None, publishNumber=None, publishDate=None, proposerName=None,
                 inventorName=None, priorityNumber=None, priorityDate=None, abstract=None, claim=None,
                 instructions=None, keyword=None, inventionType=None, publishCountry=None):
        # 申请号
        self.requestNumber = requestNumber
        # 申请日
        self.requestDate = requestDate
        # 公开（公告）号
        self.publishNumber = publishNumber
        # 公开（公告）日
        self.publishDate = publishDate
        # 申请（专利权）人
        self.proposerName = proposerName
        # 发明人
        self.inventorName = inventorName
        # 优先权号
        self.priorityNumber = priorityNumber
        # 优先权日
        self.priorityDate = priorityDate
        # 摘要
        self.abstract = abstract
        # 权利要求
        self.claim = claim
        # 说明书
        self.instructions = instructions
        # 关键词
        self.keyword = keyword
        # 发明类型
        self.inventionType = inventionType
        # 公开国
        self.publishCountry = publishCountry


