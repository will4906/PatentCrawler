# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PatentcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # 专利名称
    name = scrapy.Field()
    # 类型（公告，授权公告）
    type = scrapy.Field()
    # 专利类型
    patentType = scrapy.Field()
    # 申请号
    requestNumber = scrapy.Field()
    # 申请日
    requestDate = scrapy.Field()
    # 公布日
    publishDate = scrapy.Field()
    # 公布号
    publishNumber = scrapy.Field()
    # 申请（专利权）人
    proposerName = scrapy.Field()
    # 发明人
    inventorName = scrapy.Field()
    # 法律状态
    lawState = scrapy.Field()
    # 法律状态日期
    lawStateDate = scrapy.Field()
    # IPC分类号
    ipcNumber = scrapy.Field()
    # 代理人
    agent = scrapy.Field()
    # 代理机构
    agency = scrapy.Field()
    # 外观设计洛迦诺分类号
    locarnoNumber = scrapy.Field()
    '''一下内容为查重标志'''
    # 目标申请人
    targetProposer = scrapy.Field()
    # 目标发明人
    targetInventor = scrapy.Field()

