# -*- coding: utf-8 -*-
import json

import math

import os
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request

from PatentCrawler.items import PatentCrawlerItem, SipoCrawlerItem
from config import url_config
from config.base_settings import DATABASE_NAME
from config.query_config import QUERY_LIST
from service.CookieService import CookieService
from service.itemcollection import ItemCollection
from service.SearchService import SearchService
from visual.map_charts import ChinaMap


class PatentSpider(scrapy.Spider):
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    sipoList = QUERY_LIST

    def start_requests(self):
        indexurl = url_config.index.get('url')
        return [Request(indexurl,
                        callback=self.parse)]

    def parse(self, response):
        pre_execute = url_config.preExecute
        yield Request(
            url=pre_execute.get('url'),
            callback=self.parseAfterSetting,
            method="POST",
            headers=pre_execute.get('headers')
        )

    def parseAfterSetting(self, response):
        print(response.body_as_unicode())
        for sipo in self.sipoList:
            mainSearch = url_config.mainSearch
            headers = mainSearch.get('headers')
            searchExpCn = sipo.search_exp_cn
            print('检索表达式--- ', searchExpCn)
            formData = mainSearch.get('formdata')
            formData.__setitem__('searchCondition.searchExp', searchExpCn)
            yield FormRequest(
                url=url_config.mainSearch.get('url'),
                callback=self.parseFirstPage,
                method="POST",
                headers=headers,
                formdata=formData,
                meta={'sipo': sipo}
            )

    # 解析第一页专利组
    def parseFirstPage(self, response):
        sipo = response.meta['sipo']
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        # 解析总专利数和专利页码数
        pageTop = soup.find(attrs={"class": "page_top"})
        pagesum = 0
        patentSum = 0
        if pageTop is None:
            print('共 0 页')
        else:
            strSum = pageTop.get_text(strip=True)
            patentSum = int(strSum[strSum[2:].find("页") + 3:strSum.find("条")])
            pagesum = int(math.ceil(patentSum / 12))
            print('共', pagesum, '页')
            searchEnDiv = soup.find(id='result_executableSearchExp')
            if searchEnDiv is None:
                return
            itemList = soup.find_all(attrs={"class": "item"})
            for item in itemList:
                sipocrawler = SipoCrawlerItem()
                itemSoup = BeautifulSoup(item.prettify(), 'lxml')
                patentid = itemSoup.find(attrs={'name': 'idHidden'}).get('value')
                nrdAn = itemSoup.find(attrs={'name': 'nrdAnHidden'}).get('value')
                nrdPn = itemSoup.find(attrs={'name': 'nrdPnHidden'}).get('value')
                sipocrawler['patent_id'] = str(patentid)
                formdata = url_config.detailSearch.get('formdata')
                formdata.__setitem__('nrdAn', str(patentid).split('.')[0])
                formdata.__setitem__('cid', str(patentid))
                formdata.__setitem__('sid', str(patentid))

                # if sipo.startIndex
                yield FormRequest(
                    url=url_config.detailSearch.get('url'),
                    formdata=formdata,
                    callback=self.parsePatentDetail,
                    meta={'sipo': sipo, 'sipocrawler': sipocrawler, 'lawinfo': {'nrdAn': nrdAn, 'nrdPn': nrdPn}}
                )

            for index in range(1, pagesum):
                formdata = url_config.pageTurning.get('formdata')
                formdata.__setitem__('resultPagination.start', str(12 * index))
                formdata.__setitem__('resultPagination.totalCount', str(patentSum))
                formdata.__setitem__('searchCondition.searchExp', sipo.search_exp_cn)
                formdata.__setitem__('searchCondition.executableSearchExp', searchEnDiv.get_text())
                yield FormRequest(
                    url=url_config.pageTurning.get('url'),
                    callback=self.parseNotFirstPage,
                    method="POST",
                    headers=url_config.pageTurning.get('headers'),
                    formdata=formdata,
                    meta={
                        'sipo': sipo
                    }
                )

    # 解析非第一页专利组
    def parseNotFirstPage(self, response):
        sipo = response.meta['sipo']
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        itemList = soup.find_all(attrs={"class": "item"})
        for item in itemList:
            sipocrawler = SipoCrawlerItem()
            itemSoup = BeautifulSoup(item.prettify(), 'lxml')
            patentid = itemSoup.find(attrs={'name': 'idHidden'}).get('value')
            nrdAn = itemSoup.find(attrs={'name': 'nrdAnHidden'}).get('value')
            nrdPn = itemSoup.find(attrs={'name': 'nrdPnHidden'}).get('value')
            sipocrawler['patent_id'] = str(patentid)
            formdata = url_config.detailSearch.get('formdata')
            formdata.__setitem__('nrdAn', str(patentid).split('.')[0])
            formdata.__setitem__('cid', str(patentid))
            formdata.__setitem__('sid', str(patentid))
            yield FormRequest(
                url=url_config.detailSearch.get('url'),
                formdata=formdata,
                callback=self.parsePatentDetail,
                meta={'sipo': sipo, 'sipocrawler': sipocrawler, 'lawinfo': {'nrdAn': nrdAn, 'nrdPn': nrdPn}}
            )

    # 解析专利详情
    def parsePatentDetail(self, response):
        sipo = response.meta['sipo']
        sipocrawler = response.meta['sipocrawler']
        detail = json.loads(response.body_as_unicode())
        sipocrawler['abstract'] = BeautifulSoup(detail.get('abstractInfoDTO').get('abIndexList')[0].get('value'),
                                                'lxml').text.replace('\n', '').strip()
        sipocrawler['invention_name'] = detail.get('abstractInfoDTO').get('tioIndex').get('value')
        for abitem in detail.get('abstractInfoDTO').get('abstractItemList'):
            ItemCollection.resolveData(sipocrawler, abitem.get('indexCnName'), abitem.get('value'))
        lawinfo = response.meta.get('lawinfo')
        formdata = url_config.relatedInfo.get('formdata')
        formdata.__setitem__('literaInfo.nrdAn', lawinfo.get('nrdAn'))
        formdata.__setitem__('literaInfo.nrdPn', lawinfo.get('nrdPn'))
        yield FormRequest(
            url=url_config.relatedInfo.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=formdata,
            callback=self.parseRelatedInfo,
            meta={'sipo': sipo, 'sipocrawler': sipocrawler}
        )

    # 解析相关信息
    def parseRelatedInfo(self, response):
        related = json.loads(response.body_as_unicode())
        sipocrawler = response.meta['sipocrawler']
        lawStateList = related.get('lawStateList')
        try:
            sipocrawler['legal_status'] = lawStateList[-1].get('lawStateCNMeaning')
            sipocrawler['legal_status_effective_date'] = lawStateList[-1].get('prsDate')
        except Exception as e:
            print(lawStateList)
        yield sipocrawler

    def closed(self, reason):
        if os.path.exists(DATABASE_NAME):
            ChinaMap().create()
        print(reason)
