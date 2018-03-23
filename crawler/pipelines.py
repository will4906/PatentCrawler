# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy
import sqlite3

from logbook import Logger

from config import base_settings as bs
from entity.models import Patents
from service import info

logger = Logger(__name__)


class CrawlerPipeline(object):
    LINE_INDEX = 1

    def process_item(self, item, spider):
        data = item.get('data').__dict__
        table_dict = {}
        logger.info('采集内容：%s' % str(data))
        for name, fields in info.data_table.items():
            table_list = [[]]

            for key, value in data.items():
                if not isinstance(value, list):
                    if value.table == name or value.title in info.required_list:
                        for t in table_list:
                            t.append(value.value)
                else:
                    old = copy.deepcopy(table_list[0])
                    for list_index, value_list in enumerate(value):
                        if not isinstance(value_list, list):
                            value_list = [value_list]

                        for vi, va in enumerate(value_list):
                            part_list = []
                            for v in va:
                                if v.table == name or v.title in info.required_list:
                                    part_list.append(v.value)
                            if len(part_list) == 0:
                                break
                            if list_index > 0:
                                table_list.append(old)
                            table_list[-1] = old + part_list
            table_dict.__setitem__(name, table_list)
        conn = sqlite3.connect(bs.DATABASE_NAME)
        cursor = conn.cursor()
        for table_name, content_list in table_dict.items():
            for content in content_list:
                sql_line = 'INSERT INTO %s(' % (table_name, )
                for title in info.data_table.get(table_name):
                    sql_line += title + ', '
                sql_line = sql_line[:-2] + ') VALUES('
                for c in content:
                    sql_line += "'%s', " % c
                sql_line = sql_line[:-2] + ');'
                logger.info(sql_line)
                cursor.execute(sql_line)
                conn.commit()
        conn.close()

        return item


if __name__ == '__main__':
    tmp = {'patent_id': {'table': 'main', 'title': 'patent_id', 'value': 'CN201710311057.720170915FM'},
           'patent_name': {'table': 'main', 'title': '专利名称', 'value': '一种影像引导方法及装置'},
           'request_number': {'table': 'main', 'title': '申请号', 'value': 'CN201710311057.7'},
           'request_date': {'table': 'main', 'title': '申请日', 'value': '2017.05.05'},
           'abstract': {'table': 'main', 'title': '摘要',
                        'value': '本发明公开了一种影像引导方法及装置，所述装置包括：用于控制直线加速器产生脉冲式X射线的直线加速器控制台；用于接收放疗过程中肿瘤部位的组织产生的光声信号的超声探头；用于固定超声探的定位支架；用于放大光声信号的前置放大电路；用于采集光声信号的光声信号采集组件；用于控制光声信号采集组件在预定时间采集前置放大电路的光声信号的同步触发电路；用于接收光声信号采集组件采集的数据，并将采集的数据进行滤波、去噪处理，通过光声成像算法得到反映组织中X射线剂量分布的光声图像的计算机。本发明的影像引导装置可作为放疗的实时影像引导设备，是一种经济、无创、无辐射的影像引导技术，所述装置可提供剂量图像引导放疗。'},
           'law_state_list': [{'table': 'law_state', 'title': '法律状态', 'value': '发明专利申请公布'},
                              {'table': 'law_state', 'title': '法律状态时间', 'value': '20170915'},
                              {'table': 'law_state', 'title': '法律状态', 'value': '实质审查的生效'},
                              {'table': 'law_state', 'title': '法律状态时间', 'value': '20171017'}]}
    CrawlerPipeline().process_item(None, None)
    # t = [1, 2]
    # t2 = 1
    # print(list(t))
    # print(list(t2))
