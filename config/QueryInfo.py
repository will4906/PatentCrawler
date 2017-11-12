# -*- coding: utf-8 -*-
"""
Created on 2017/3/24

@author: will4906
"""
from entity.query_item import SipoItem, DateSelect, And, ItemGroup, Or, Not


class SipoTarget:
    def __init__(self):
        self.queryList = [
            SipoItem(inventor='陈思平', proposer='深圳大学', publish_date=DateSelect('>=', '2001-01-01'),
                     invention_type='实用新型', publish_country='HK'),
            SipoItem(inventor='陈思平', proposer='深圳大学', publish_date=DateSelect('>=', '2001-01-01'),
                     invention_type='发明申请', publish_country='HK'),
            SipoItem(inventor='陈思平', proposer='深圳大学', publish_date=DateSelect('>=', '2001-01-01'),
                     invention_type='外观设计', publish_country='HK'),
        ]

