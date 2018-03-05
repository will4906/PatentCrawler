# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from logbook import Logger

from entity.models import Patents

logger = Logger(__name__)


class CrawlerPipeline(object):
    LINE_INDEX = 1

    def process_item(self, item, spider):
        patent_detail = item.__dict__.get('_values')
        try:
            Patents.insert_many(patent_detail).execute()
        except Exception as e:
            print(e)
        logger.info('第 %s 个专利采集结束(patent_id: %s, invention_name: %s)' % (CrawlerPipeline.LINE_INDEX,
        patent_detail.get('patent_id'), patent_detail.get('invention_name')))
        CrawlerPipeline.LINE_INDEX += 1
        return item
