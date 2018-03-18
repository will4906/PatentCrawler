# -*- coding: utf-8 -*-
"""
Created on 2018/3/12

@author: will4906
"""
import configparser
import copy
import inspect
import sqlite3

from config import crawler_config
from config import base_settings as bs
from controller.url_config import *
from config.crawler_config import *
from entity.crawler_item import BaseItem

crawler_dict = {
    url_search.get('crawler_id'): [],
    url_detail.get('crawler_id'): [],
    url_related_info.get('crawler_id'): [],
    url_full_text.get('crawler_id'): [],
    '4': []
}
data_table = {}
required_list = []


def init_crawler(cfg: configparser.ConfigParser):
    try:
        content_items = str(cfg.get('crawler', 'content'))
        content_items = content_items.replace(' ', '')
        content_item_list = content_items[1:-1].split(',')
        result = ''
        for item in content_item_list:
            result += "'" + item + "',"
        result = content_items[0] + result + content_items[-1]
        content_items = eval(result)
        if isinstance(content_items, list):
            gen_crawler_list(content_items)
        else:
            raise Exception('items error')
    except:
        gen_crawler_list([
            'patent_id', 'invention_name', 'request_number', 'request_date', 'publish_number', 'publish_date',
            'proposer', 'inventor', 'abstract'
        ])
    print(crawler_dict)
    create_tables()


def gen_crawler_list(content_list):
    tmp_list = push_crawler_list()
    for content in content_list:
        for tmp in tmp_list:
            has_chinese = tmp.check_chinese(content)
            has_english = tmp.check_english(content)
            if has_chinese or has_english:
                tmp.set_title(content)
                crawler_dict.get(str(tmp.crawler_id)).append(tmp)
                break
    for tmp in tmp_list:
        if tmp.is_required and tmp not in crawler_dict.get(str(tmp.crawler_id)):
            tmp.set_title(tmp.english)
            crawler_dict.get(str(tmp.crawler_id)).append(tmp)
        if tmp.is_required:
            required_list.append(tmp.title)


def push_crawler_list():
    tmp_list = []
    for item in dir(crawler_config):
        try:
            t = eval(item)
            if inspect.isclass(t):
                if BaseItem in t.__bases__:
                    tmp_list.append(t)
        except:
            pass
    return tmp_list


def create_tables():
    """
    创建表格的函数
    :return:
    """
    conn = sqlite3.connect(bs.DATABASE_NAME)
    cursor = conn.cursor()
    table_dict = {}
    for key, value in crawler_dict.items():
        for v in value:
            table = table_dict.get(v.table_name)
            if table is None:
                tmp_list = copy.copy(required_list)
                if not v.is_required:
                    if isinstance(v.title, str):
                        tmp_list.append(v.title)
                    elif isinstance(v.title, list):
                        for t in v.title:
                            tmp_list.append(t)
                table_dict.__setitem__(v.table_name, tmp_list)
            else:
                if not v.is_required:
                    if isinstance(v.title, str):
                        table.append(v.title)
                    elif isinstance(v.title, list):
                        for t in v.title:
                            table.append(t)
                table_dict.__setitem__(v.table_name, table)
    global data_table
    data_table = table_dict
    for k, value in table_dict.items():
        content = 'CREATE TABLE %s ( ' % k
        for v in value:
            content += '%s VARCHAR(255), ' % v
        content = content[:-2]
        content += ');'
        cursor.execute(content)
        conn.commit()
    conn.close()


if __name__ == '__main__':
    push_crawler_list()
