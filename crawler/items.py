# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 此处英文全部匹配query_item.py里的title_define
class SipoCrawlerItem(scrapy.Item):
    # 专利id
    patent_id = scrapy.Field()
    # 申请号
    request_number = scrapy.Field()
    # 申请日
    request_date = scrapy.Field()
    # 公开（公告）号
    publish_number = scrapy.Field()
    # 公开（公告）日
    publish_date = scrapy.Field()
    # 发明名称
    invention_name = scrapy.Field()
    # IPC分类号
    ipc_class_number = scrapy.Field()
    # 申请（专利权）人
    proposer = scrapy.Field()
    # 发明人
    inventor = scrapy.Field()
    # 优先权号
    priority_number = scrapy.Field()
    # 优先权日
    priority_date = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # 权利要求
    claim = scrapy.Field()
    # 说明书
    instructions = scrapy.Field()
    # 外观设计洛迦诺分类号
    locarno_class_number = scrapy.Field()
    # 代理人
    agent = scrapy.Field()
    # 代理机构
    agency = scrapy.Field()
    # 申请人邮编
    proposer_post_code = scrapy.Field()
    # 申请人地址
    proposer_address = scrapy.Field()
    # 申请人所在国（省）
    proposer_location = scrapy.Field()
    # FT分类号
    FT_class_number = scrapy.Field()
    # UC分类号
    UC_class_number = scrapy.Field()
    # ECLA分类号
    ECLA_class_number = scrapy.Field()
    # FI分类号
    FI_class_number = scrapy.Field()
    # CPC分类号
    CPC_class_number = scrapy.Field()
    # 发明类型
    invention_type = scrapy.Field()
    # 公开国
    publish_country = scrapy.Field()
    # 法律状态
    legal_status = scrapy.Field()
    #  法律状态生效日期
    legal_status_effective_date = scrapy.Field()

    PCT_enters_national_phase_date = scrapy.Field()