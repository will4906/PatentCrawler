# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from logbook import Logger
from requests.utils import dict_from_cookiejar
from scrapy.downloadermiddlewares.retry import RetryMiddleware

import controller as ctrl
from config.base_settings import USE_PROXY
from service.account import login

logger = Logger(__name__)


class PatentMiddleware(RetryMiddleware):

    def process_request(self, request, spider):
        if USE_PROXY and ctrl.PROXIES is not None:
            request.meta['proxy'] = "http://%s" % (ctrl.PROXIES.get('http'))
        if ctrl.COOKIES is not None:
            request.cookies = dict_from_cookiejar(ctrl.COOKIES)

    def process_response(self, request, response, spider):
        body = response.body_as_unicode()
        # logger.info(body.find('window.location.href = contextPath +"/portal/uilogin-forwardLogin.shtml";'))
        # logger.info(body.find('访问受限'))
        # logger.info(response.status)
        if response.status == 404 or response.status == 417:
            pass
            # logger.info(body)
        if body.find('window.location.href = contextPath +"/portal/uilogin-forwardLogin.shtml";') != -1 or body.find(
                '访问受限') != -1 or response.status == 404:
            logger.info('未登录，登陆中，请稍后···')
            login_ok = False
            if ctrl.BEING_LOG is False:
                login_ok = login()
            while ctrl.BEING_LOG:
                time.sleep(1)
            if login_ok:
                return self._retry(request, 'unlogin', spider)
        return response

    def process_exception(self, request, exception, spider):
        logger.error(exception)
        login_ok = False
        if ctrl.BEING_LOG is False:
            login_ok = login()
        while ctrl.BEING_LOG:
            time.sleep(1)
        if login_ok:
            self._retry(request, 'unlogin', spider)
