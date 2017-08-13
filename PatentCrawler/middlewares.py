# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from service.CookieService import CookieService
from service.LoginService import LoginService
from util.HeadersEngine import HeadersEngine


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', HeadersEngine().getRandomUserAgent())


class ProxyMiddleware:
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://58.209.151.126:808"


class CookiesMiddleware:
    def process_request(self, request, spider):
        # print(request.cookies)
        pass


class MyRedirectMiddleware:
    def process_response(self, request, response, spider):
        if CookieService.getCookies() == {}:
            CookieService.getCookiesFromList(response.headers.getlist('Set-Cookie'))
            CookieService.saveCookies()
            LoginService(CookieService.getCookies()).startLogin()
        request.cookies = CookieService.getCookies()
        return response