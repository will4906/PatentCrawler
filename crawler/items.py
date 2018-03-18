# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem:

    def __repr__(self):
        return str(self.__dict__)


class WrapperItem(scrapy.Item):

    data = scrapy.Field()


if __name__ == '__main__':
    pass
    # w = WrapperItem()
    # my = MyItem()
    # my.hello = 1
    # my.good = 2
    # w['data'] = my
    # print(w)
    # sipo = SipoCrawlerItem()
    # my = MyItem()
    # my.hello = 1
    # sipo['patent_id'] = my
    # print(sipo)