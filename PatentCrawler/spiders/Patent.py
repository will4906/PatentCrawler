# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request

from PatentCrawler.items import PatentcrawlerItem
from util.HeadersEngine import HeadersEngine


class PatentSpider(scrapy.Spider):
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    start_urls = ['http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml']

    def parse(self, response):
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent" : HeadersEngine().getRandomUserAgent()
        }
        formData = {
            "searchCondition.searchExp" : "公开（公告）日>=2001-01-01 AND 申请（专利权）人=(北京科技大学) AND 发明类型=(\"I\") AND 公开国=(HK OR CN) ",
            "searchCondition.dbId": "VDB",
            "searchCondition.searchType" : "Sino_foreign",
            "searchCondition.power" : "false",
            "wee.bizlog.modulelevel" : "0200201",
            "resultPagination.limit" : "50"
        }
        formData2 = {
            "searchCondition.searchExp": "公开（公告）日>=2001-01-01 AND 申请（专利权）人=(深圳大学) AND 发明类型=(\"I\") AND 公开国=(HK OR CN) ",
            "searchCondition.dbId": "VDB",
            "searchCondition.searchType": "Sino_foreign",
            "searchCondition.power": "false",
            "wee.bizlog.modulelevel": "0200201",
            "resultPagination.limit": "50"
        }
        yield FormRequest(
            url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/biaogejsAC!executeCommandSearchUnLogin.do",
            callback=self.parsePatentList,
            method="POST",
            headers=headers,
            formdata=formData
        )
        yield FormRequest(
            url="http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/biaogejsAC!executeCommandSearchUnLogin.do",
            callback=self.parsePatentList,
            method="POST",
            headers=headers,
            formdata=formData2
        )

    def parsePatentList(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), "lxml")
        itemList = soup.find_all(attrs={"class" : "item"})
        pi = PatentcrawlerItem()
        for item in itemList:
            itemSoup = BeautifulSoup(item.prettify(), "lxml")
            header = itemSoup.find(attrs={"class" : "item-header"})
            print(header.find("h1").get_text(strip=True))
            pi['name'] = header.find("h1").get_text(strip=True)
            print(header.find(attrs={"class" : "btn-group left clear"}).get_text(strip=True))
            content = itemSoup.find(attrs={"class" : "item-content-body left"})
            contentList = content.find_all("p")
            for c in contentList:
                print(c.get_text(strip=True))
