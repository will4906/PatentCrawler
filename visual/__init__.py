# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

绘图模块
"""
import os

from datetime import datetime
from logbook import Logger
from pyecharts import Map, Page, Bar

from config.base_settings import CHARTS_NAME
from entity.models import Patents


logger = Logger(__name__)


def create_charts():
    page = Page()
    page.add(create_map())
    page.add(create_year_bar())
    page.render(CHARTS_NAME)
    logger.info("图表绘制完成")


def create_map():
    province_list = [
            '北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东'
            , '新疆', '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建'
            , '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门'
        ]
    value_list = []
    max_value = 0
    for i, province in enumerate(province_list):
        province_counts = Patents.select().where(Patents.proposer_address ** ('%' + province + '%')).count()
        if max_value < province_counts:
            max_value = province_counts
        value_list.append(province_counts)

    map = Map("专利省份分布地图", width=1200, height=600)
    map.add('', province_list, value_list, maptype='china', is_visualmap=True, is_label_show=True, visual_text_color='#000', visual_range=[0, max_value])
    return map


def create_year_bar():
    bar = Bar("专利年份分布", width=1200, height=600)

    year_dicts = {}
    for date in Patents.select(Patents.request_date).dicts():
        if date.get('request_date', '') != '':
            date_time = datetime.strptime(date.get('request_date', ''), '%Y.%m.%d')
            year_patents = year_dicts.get(date_time.year, 0)
            year_patents += 1
            year_dicts.__setitem__(date_time.year, year_patents)
    year_list = []
    count_list = []
    for year, counts in year_dicts.items():
        year_list.append(year)

    year_list.sort()
    for year in year_list:
        count_list.append(year_dicts.get(year))

    bar.add('申请', year_list, count_list)

    year_dicts = {}
    for date in Patents.select(Patents.publish_date).dicts():
        if date.get('publish_date', '') != '':
            date_time = datetime.strptime(date.get('publish_date', ''), '%Y.%m.%d')
            year_patents = year_dicts.get(date_time.year, 0)
            year_patents += 1
            year_dicts.__setitem__(date_time.year, year_patents)
    year_list = []
    count_list = []
    for year, counts in year_dicts.items():
        year_list.append(year)

    year_list.sort()
    for year in year_list:
        count_list.append(year_dicts.get(year))

    bar.add('公告', year_list, count_list)
    return bar
