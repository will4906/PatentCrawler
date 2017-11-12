# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.downloadermiddlewares.retry import RetryMiddleware
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


class NormalMiddleware:

    def process_request(self, request, spider):
        request.cookies = CookieService.cookies


class UnloginRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if response.status == 200:
            ok = CookieService.checkWholeCookieFromSetCookies(response.headers.getlist('Set-Cookie'))
            if ok is True:
                CookieService.readCookiesFromList(response.headers.getlist('Set-Cookie'))
        if response.status == 302:
            LoginService(CookieService.cookies).startLogin()
            request.cookies = CookieService.cookies
            self._retry(request, 'unlogin', spider)
        return response
