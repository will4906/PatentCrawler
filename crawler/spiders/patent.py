import json

import math

import os
import scrapy
import webbrowser
from bs4 import BeautifulSoup
from logbook import Logger
from scrapy import Request, FormRequest

from config.base_settings import *
from config.query_config import QUERY_LIST
from controller.url_config import *
from crawler.items import DataItem, WrapperItem
from service import info
from visual import create_charts

logger = Logger(__name__)


class PatentSpider(scrapy.Spider):
    """
    专利网爬虫定义
    """
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    query_list = QUERY_LIST
    process_len = 4

    def __init__(self, *args, **kwargs):
        self.target_dict = {
            url_detail.get('crawler_id'): self.gen_detail,
            url_related_info.get('crawler_id'): self.gen_related_info,
            url_full_text.get('crawler_id'): self.gen_full_text
        }
        super().__init__(*args, **kwargs)

    def gen_detail(self, **kwargs):
        """
        生成查询详情的请求
        :param patent_id, sipo, data_item, nrdAn, nrdPn:
        :return:
        """
        patent_id = str(kwargs.pop('patent_id'))
        formdata = url_detail.get('form_data')
        formdata.__setitem__('nrdAn', patent_id.split('.')[0])
        formdata.__setitem__('cid', patent_id)
        formdata.__setitem__('sid', patent_id)

        return FormRequest(
            url=url_detail.get('url'),
            formdata=formdata,
            callback=self.parse_patent_detail,
            meta={'sipo': kwargs.pop('sipo'), 'data_item': kwargs.pop('data_item'), 'patent_id': patent_id,
                  'law_info': {'nrdAn': kwargs.pop('nrdAn'), 'nrdPn': kwargs.pop('nrdPn')}}
        )

    def gen_related_info(self, **kwargs):
        """
        生成相关信息的请求，包含法律信息和同族信息
        :param sipo:
        :param data_item:
        :param nrdAn:
        :param nrdPn:
        :return:
        """
        form_data = url_related_info.get('form_data')
        form_data.__setitem__('literaInfo.nrdAn', kwargs.pop('nrdAn'))
        form_data.__setitem__('literaInfo.nrdPn', kwargs.pop('nrdPn'))
        return FormRequest(
            url=url_related_info.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=form_data,
            callback=self.parse_related_info,
            meta={'sipo': kwargs.pop('sipo'), 'data_item': kwargs.pop('data_item'), 'patent_id': kwargs.pop('patent_id')}
        )

    def gen_full_text(self, **kwargs):
        """
        生成全文文本的请求
        :param patent_id:
        :param sipo:
        :param data_item:
        :return:
        """
        patent_id = str(kwargs.pop('patent_id'))
        form_data = url_full_text.get('form_data')
        form_data.__setitem__('nrdAn', patent_id.split('.')[0])
        form_data.__setitem__('cid', patent_id)
        form_data.__setitem__('sid', patent_id)
        return FormRequest(
            url=url_full_text.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=form_data,
            callback=self.parse_full_text,
            meta={'sipo': kwargs.pop('sipo'), 'data_item': kwargs.pop('data_item')}
        )

    def gen_wrapper_item(self, data_item):
        """
        生成包裹的采集对象
        :param data_item:
        :return:
        """
        wrapper = WrapperItem()
        wrapper['data'] = data_item
        return wrapper

    def turn_to_request(self, now, **kwargs):
        """
        下一可采集请求的生成转换逻辑
        :param now:
        :param kwargs:
        :return:
        """
        next_target = now
        for i in range(now + 1, self.process_len):
            target_len = len(info.crawler_dict.get(str(i)))
            if target_len > 0:
                next_target = i
                break
        if next_target == now:
            data_item = kwargs.pop('data_item')
            return self.gen_wrapper_item(data_item)
        else:
            return self.target_dict.get(str(next_target))(**kwargs)

    def start_requests(self):
        """
        初始请求
        :return:
        """
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
        """
        解析请求结果第一页
        :param response:
        :return:
        """
        body = response.body_as_unicode()
        sipo = response.meta['sipo']
        soup = BeautifulSoup(body, 'lxml')
        # 解析总专利数和专利页码数
        page_top = soup.find(attrs={"class": "page_top"})
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
                data_item = DataItem()
                itemSoup = BeautifulSoup(item.prettify(), 'lxml')

                for crawler in info.crawler_dict.get('0'):
                    crawler.parse(item.prettify(), data_item, itemSoup)

                patent_id = itemSoup.find(attrs={'name': 'idHidden'}).get('value')
                nrdAn = itemSoup.find(attrs={'name': 'nrdAnHidden'}).get('value')
                nrdPn = itemSoup.find(attrs={'name': 'nrdPnHidden'}).get('value')

                yield self.turn_to_request(int(url_search.get('crawler_id')), data_item=data_item, nrdAn=nrdAn, nrdPn=nrdPn, patent_id=patent_id, sipo=sipo)

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
        """
        解析请求结果非首页
        :param response:
        :return:
        """
        sipo = response.meta['sipo']
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        itemList = soup.find_all(attrs={"class": "item"})
        for item in itemList:
            data_item = DataItem()
            itemSoup = BeautifulSoup(item.prettify(), 'lxml')
            patent_id = itemSoup.find(attrs={'name': 'idHidden'}).get('value')
            nrdAn = itemSoup.find(attrs={'name': 'nrdAnHidden'}).get('value')
            nrdPn = itemSoup.find(attrs={'name': 'nrdPnHidden'}).get('value')

            for crawler in info.crawler_dict.get(url_page_turning.get('crawler_id')):
                crawler.parse(item.prettify(), data_item, itemSoup)

            yield self.turn_to_request(int(url_page_turning.get('crawler_id')), patent_id=patent_id, nrdPn=nrdPn, nrdAn=nrdAn, sipo=sipo, data_item=data_item)

    def parse_patent_detail(self, response):
        """
        解析专利详情页
        :param response:
        :return:
        """
        sipo = response.meta['sipo']
        data_item = response.meta['data_item']
        patent_id = response.meta['patent_id']
        body = response.body_as_unicode()
        detail = json.loads(body)

        for crawler in info.crawler_dict.get(url_detail.get('crawler_id')):
            crawler.parse(body, data_item, detail)

        law_info = response.meta.get('law_info')
        yield self.turn_to_request(int(url_detail.get('crawler_id')), nrdAn=law_info.get('nrdAn'), nrdPn=law_info.get('nrdPn'), sipo=sipo, data_item=data_item, patent_id=patent_id)

    def parse_related_info(self, response):
        """
        解析相关信息页
        :param response:
        :return:
        """
        body = response.body_as_unicode()
        related = json.loads(body)
        data_item = response.meta['data_item']
        sipo = response.meta['sipo']
        patent_id = response.meta['patent_id']

        for crawler in info.crawler_dict.get(url_related_info.get('crawler_id')):
            crawler.parse(body, data_item, related)

        yield self.turn_to_request(int(url_related_info.get('crawler_id')), data_item=data_item, sipo=sipo, patent_id=patent_id)

    def parse_full_text(self, response):
        """
        解析全文文本页
        :param response:
        :return:
        """
        data_item = response.meta['data_item']
        yield self.turn_to_request(int(url_full_text.get('crawler_id')), data_item=data_item)

    def closed(self, reason):
        webbrowser.open(AD_PATH)
        # if os.path.exists(DATABASE_NAME) and 'data' in OUTPUT_ITEMS and 'chart' in OUTPUT_ITEMS:
        #     create_charts()
        logger.info(reason)
