# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from util.HeadersEngine import HeadersEngine


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', HeadersEngine().getRandomUserAgent())


class ProxyMiddleware:

    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://58.209.151.126:808"