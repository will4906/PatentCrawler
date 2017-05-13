# -*- coding: utf-8 -*-
"""
Created on 2017/5/14

@author: will4906
"""


class SearchService:

    @staticmethod
    def getCnSearchExp(startDate, proposer, inventor, type):
        searchExp = "公开（公告）日>=" + startDate
        if proposer != "":
            searchExp += " AND 申请（专利权）人=(" + proposer + ")"
        if inventor != "":
            searchExp += " AND 发明人=(" + inventor + ")"
        searchExp += " AND 发明类型=(\"" + type + "\") AND 公开国=(HK OR MO OR TW OR CN)"
        return searchExp

    @staticmethod
    def getEnSearchExp(startDate, proposer, inventor, type):
        searchExp = "VDB:((PD>='" + startDate + "'"
        if proposer != "":
            searchExp += " AND PAVIEW='" + proposer + "'"
        if inventor != "":
            searchExp += " AND INVIEW='" + inventor + "'"
        searchExp += " AND DOC_TYPE='" + type + "' AND (CC='HK' OR CC='MO' OR CC='TW' OR CC='CN')))"
        return searchExp
