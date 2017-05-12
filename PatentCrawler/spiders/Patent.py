# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request

from PatentCrawler.items import PatentcrawlerItem
from config.BaseConfig import BaseConfig
from config.QueryInfo import QueryInfo
from service.ItemCollection import ItemCollection
from util.HeadersEngine import HeadersEngine


class PatentSpider(scrapy.Spider):
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    start_urls = ['http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml']
    queryInfo = QueryInfo()
    inventorList = queryInfo.getInventorList()
    inventionTypeList = queryInfo.getInventionTypeList()
    proposer = queryInfo.getProposer()
    startDate = queryInfo.getStartDate()

    def parse(self, response):
        for inventor in self.inventorList:
            for type in self.inventionTypeList:
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": HeadersEngine().getRandomUserAgent()
                }
                searchExp = "公开（公告）日>=" + self.startDate + " AND 申请（专利权）人=(" + self.proposer + ") AND 发明人=(" + inventor + ") AND 发明类型=(\"" + type + "\") AND 公开国=(HK OR MO OR TW OR CN)"
                formData = {
                    "searchCondition.searchExp": searchExp,
                    "searchCondition.dbId": "VDB",
                    "searchCondition.searchType": "Sino_foreign",
                    "searchCondition.power": "false",
                    "wee.bizlog.modulelevel": "0200201",
                    "resultPagination.limit": BaseConfig.CRAWLER_SPEED
                }
                yield FormRequest(
                    url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/biaogejsAC!executeCommandSearchUnLogin.do",
                    callback=self.parsePatentList,
                    method="POST",
                    headers=headers,
                    formdata=formData,
                    meta={
                        'searchExp': searchExp,
                        'inventionType': type,
                        'startDate' : self.startDate,
                        'proposer' : self.proposer,
                        'inventor' : inventor
                    }
                )

    # 解析专利组
    def parsePatentList(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), "lxml")
        type = response.meta['inventionType']
        pageTop = soup.find(attrs={"class" : "page_top"})
        patentSum = int(pageTop.get_text(strip=True)[8:-3])
        if(patentSum % int(BaseConfig.CRAWLER_SPEED)) == 0:
            scale = 0
        else:
            scale = 1
        roundSum = int(patentSum / int(BaseConfig.CRAWLER_SPEED)) + scale
        for index in range(1, roundSum):
            yield self.requestNextPage(response.meta['searchExp'], index, patentSum, response.meta['startDate'], response.meta['proposer'], response.meta['inventor'], type)
        itemList = soup.find_all(attrs={"class" : "item"})
        pi = PatentcrawlerItem()
        for item in itemList:
            itemSoup = BeautifulSoup(item.prettify(), "lxml")
            header = itemSoup.find(attrs={"class" : "item-header"})
            pi['name'] = header.find("h1").get_text(strip=True)
            pi['type'] = header.find(attrs={"class" : "btn-group left clear"}).get_text(strip=True)
            pi['patentType'] = QueryInfo.inventionTypeToString(type)
            content = itemSoup.find(attrs={"class" : "item-content-body left"})
            contentList = content.find_all("p")
            for c in contentList:
                ItemCollection.resolveData(pi, c.get_text(strip=True))
            footer = itemSoup.find(attrs={"class" : "item-footer"})
            lawStateBn = footer.find(attrs={"role" : "lawState"})
            yield self.requestLawState(lawStateBn, pi)

    # 解析翻页后的专利数据
    def parseNextPatentList(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), "lxml")
        type = response.meta['inventionType']
        itemList = soup.find_all(attrs={"class": "item"})
        pi = PatentcrawlerItem()
        for item in itemList:
            itemSoup = BeautifulSoup(item.prettify(), "lxml")
            header = itemSoup.find(attrs={"class": "item-header"})
            pi['name'] = header.find("h1").get_text(strip=True)
            pi['type'] = header.find(attrs={"class": "btn-group left clear"}).get_text(strip=True)
            pi['patentType'] = QueryInfo.inventionTypeToString(type)
            content = itemSoup.find(attrs={"class": "item-content-body left"})
            contentList = content.find_all("p")
            for c in contentList:
                ItemCollection.resolveData(pi, c.get_text(strip=True))
            footer = itemSoup.find(attrs={"class": "item-footer"})
            lawStateBn = footer.find(attrs={"role": "lawState"})
            yield self.requestLawState(lawStateBn, pi)

    # 解析法律信息，并且将item交个pipeLine
    def parseLawState(self, response):
        item = response.meta
        try:
            result = json.loads(response.body_as_unicode())
            pi = PatentcrawlerItem()
            item['lawState'] = result['lawStateList'][-1]['lawStateCNMeaning']
            item['lawStateDate'] = result['lawStateList'][-1]['prsDate']
            ItemCollection.addCrawlerItem(pi, item)
            yield pi
        except:
            print("速度太快")

    # 发送法律信息的请求
    def requestLawState(self, lawStateBn, pi):
        lawFormData = {
            'lawState.nrdPn': lawStateBn['pn'],
            'lawState.nrdAn': lawStateBn['an'],
            'wee.bizlog.modulelevel': '0202201',
            'pagination.start': '0'
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": HeadersEngine().getRandomUserAgent()
        }
        return FormRequest(
            url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/ui_searchLawState-showPage.shtml",
            callback=self.parseLawState,
            method="POST",
            headers=headers,
            formdata=lawFormData,
            meta=pi
        )

    # 生成接下来专利信息的请求
    def requestNextPage(self, searchExp, index, nSum, startDate, proposer, inventor, type):
        formData = {
            "resultPagination.limit": BaseConfig.CRAWLER_SPEED,
            "resultPagination.start": str(int(BaseConfig.CRAWLER_SPEED) * index),
            "resultPagination.totalCount": str(nSum),
            "searchCondition.searchType": "Sino_foreign",
            "searchCondition.dbId": "",
            "searchCondition.power": "false",
            "searchCondition.searchExp": searchExp,
            "searchCondition.executableSearchExp": "VDB:((PD>='" + startDate + "' AND PAVIEW='" + proposer + "' AND INVIEW='" + inventor + "' AND DOC_TYPE='" + type + "' AND (CC='HK' OR CC='MO' OR CC='TW' OR CC='CN')))"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": HeadersEngine().getRandomUserAgent()
        }
        return FormRequest(
                    url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml",
                    callback=self.parseNextPatentList,
                    method="POST",
                    headers=headers,
                    formdata=formData,
                    meta={
                        'inventionType': type
                    }
                )