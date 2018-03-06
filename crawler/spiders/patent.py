import json

import math

import os
import scrapy
from bs4 import BeautifulSoup
from logbook import Logger
from scrapy import Request, FormRequest

from config.base_settings import *
from config.query_config import QUERY_LIST
from controller.url_config import *
from crawler.items import SipoCrawlerItem
from service.item_collection import resolve_data
from visual.map_charts import ChinaMap

logger = Logger(__name__)


class PatentSpider(scrapy.Spider):
    """
    专利网爬虫定义
    """
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    query_list = QUERY_LIST

    def start_requests(self):
        for sipo in self.query_list:
            headers = url_search.get('headers')
            search_exp_cn = sipo.search_exp_cn
            logger.info('检索表达式--- %s' % search_exp_cn)
            form_data = url_search.get('form_data')
            form_data.__setitem__('searchCondition.searchExp', search_exp_cn)
            yield FormRequest(
                url=url_search.get('url'),
                callback=self.parse,
                method="POST",
                headers=headers,
                formdata=form_data,
                meta={'sipo': sipo}
            )

    def parse(self, response):
        body = response.body_as_unicode()
        sipo = response.meta['sipo']
        soup = BeautifulSoup(body, 'lxml')
        # 解析总专利数和专利页码数
        page_top = soup.find(attrs={"class": "page_top"})
        page_sum = 0
        patent_sum = 0
        if page_top == 0:
            logger.info('共0页')
        else:
            page_top_line = page_top.get_text(strip=True)
            patent_sum = int(page_top_line[page_top_line[2:].find("页") + 3:page_top_line.find("条")])
            page_sum = int(math.ceil(patent_sum / 12))
            logger.info('共 %s 页' % page_sum)
            search_en_div = soup.find(id='result_executableSearchExp')
            if search_en_div is None:
                return
            item_list = soup.find_all(attrs={"class": "item"})
            for item in item_list:
                sipocrawler = SipoCrawlerItem()
                itemSoup = BeautifulSoup(item.prettify(), 'lxml')
                patentid = itemSoup.find(attrs={'name': 'idHidden'}).get('value')
                nrdAn = itemSoup.find(attrs={'name': 'nrdAnHidden'}).get('value')
                nrdPn = itemSoup.find(attrs={'name': 'nrdPnHidden'}).get('value')
                sipocrawler['patent_id'] = str(patentid)
                formdata = url_detail.get('form_data')
                formdata.__setitem__('nrdAn', str(patentid).split('.')[0])
                formdata.__setitem__('cid', str(patentid))
                formdata.__setitem__('sid', str(patentid))

                yield FormRequest(
                    url=url_detail.get('url'),
                    formdata=formdata,
                    callback=self.parse_patent_detail,
                    meta={'sipo': sipo, 'sipocrawler': sipocrawler, 'lawinfo': {'nrdAn': nrdAn, 'nrdPn': nrdPn}}
                )

            for index in range(1, page_sum):
                formdata = url_page_turning.get('form_data')
                formdata.__setitem__('resultPagination.start', str(12 * index))
                formdata.__setitem__('resultPagination.totalCount', str(patent_sum))
                formdata.__setitem__('searchCondition.searchExp', sipo.search_exp_cn)
                formdata.__setitem__('searchCondition.executableSearchExp', search_en_div.get_text())
                yield FormRequest(
                    url=url_page_turning.get('url'),
                    callback=self.parse_not_first_page,
                    method="POST",
                    headers=url_page_turning.get('headers'),
                    formdata=formdata,
                    meta={
                        'sipo': sipo
                    }
                )

    def parse_not_first_page(self, response):
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
            formdata = url_detail.get('form_data')
            formdata.__setitem__('nrdAn', str(patentid).split('.')[0])
            formdata.__setitem__('cid', str(patentid))
            formdata.__setitem__('sid', str(patentid))
            yield FormRequest(
                url=url_detail.get('url'),
                formdata=formdata,
                callback=self.parse_patent_detail,
                meta={'sipo': sipo, 'sipocrawler': sipocrawler, 'lawinfo': {'nrdAn': nrdAn, 'nrdPn': nrdPn}}
            )

    def parse_patent_detail(self, response):
        sipo = response.meta['sipo']
        sipocrawler = response.meta['sipocrawler']
        detail = json.loads(response.body_as_unicode())
        sipocrawler['abstract'] = BeautifulSoup(detail.get('abstractInfoDTO').get('abIndexList')[0].get('value'),
                                                'lxml').text.replace('\n', '').strip()
        sipocrawler['invention_name'] = detail.get('abstractInfoDTO').get('tioIndex').get('value')
        logger.info('开始采集(patent_id: %s, invention_name: %s)' % (
        sipocrawler.get('patent_id'), sipocrawler.get('invention_name')))
        for abitem in detail.get('abstractInfoDTO').get('abstractItemList'):
            try:
                resolve_data(sipocrawler, abitem.get('indexCnName'), abitem.get('value'))
            except Exception as e:
                logger.warn('无法支持 %s 字段' % abitem.get('indexCnName'))
        lawinfo = response.meta.get('lawinfo')
        formdata = url_related_info.get('form_data')
        formdata.__setitem__('literaInfo.nrdAn', lawinfo.get('nrdAn'))
        formdata.__setitem__('literaInfo.nrdPn', lawinfo.get('nrdPn'))
        yield FormRequest(
            url=url_related_info.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=formdata,
            callback=self.parse_related_info,
            meta={'sipo': sipo, 'sipocrawler': sipocrawler}
        )

    def parse_related_info(self, response):
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
        if os.path.exists(DATABASE_NAME) and 'data' in OUTPUT_ITEMS and 'chart' in OUTPUT_ITEMS:
            ChinaMap().create()
        logger.info(reason)
