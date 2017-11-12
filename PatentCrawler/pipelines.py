# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from peewee import InsertQuery

from config.BaseConfig import BaseConfig
from entity.models import Patents
from util.excel.ExcelUtil import ExcelUtil


class PatentcrawlerPipeline(object):

    LINE_INDEX = 1

    def process_item(self, item, spider):
        print(item.__dict__)
        try:
            iq = InsertQuery(Patents, item.__dict__.get('_values'))
            iq.execute()
        except Exception as e:
            print(e)
        return item

