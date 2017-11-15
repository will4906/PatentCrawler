# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import shutil

from entity.models import Patents
from config.base_settings import TEMPLATE_NAME, DIAGRAM_NAME


class ChinaMap:
    def __init__(self):
        self.provinceList = [
            '北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东'
            , '新疆', '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建'
            , '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门'
        ]
        self.provinceNum = {}
        self.tempValue = "{name: '{name}', value: {value}}"
        self.maxValue = 1
        self.table = Patents
        self.template = TEMPLATE_NAME

    def __getProposerDistribution(self):
        china_data = ''
        max_value = 0
        for index, province in enumerate(self.provinceList):
            pnum = Patents.select().where(Patents.proposer_address ** ('%' + province + '%')).count()
            if pnum > 0:
                china_data += self.tempValue.replace('{name}', province).replace('{value}', str(pnum)) + ','
            if max_value < pnum:
                max_value = pnum
        china_data = china_data[:len(china_data) - 1]
        return china_data, max_value

    def __replaceChinaData(self, china_data, max_value):
        with open(DIAGRAM_NAME, "r", encoding='UTF-8') as f:
            x = f.readlines()  # 读取原文件并存储于x
            with open(DIAGRAM_NAME, "w"): pass  # 清空原文件
            for i in x:
                s = i.replace('{{ chinaMap.data }}', china_data).replace('{{ chinaMap.max }}', str(max_value + 5))
                with open(DIAGRAM_NAME, "a", encoding='UTF-8') as f:
                    f.write(s)

    def create(self):
        chnia_data, max_value = self.__getProposerDistribution()
        self.__replaceChinaData(chnia_data, max_value)










