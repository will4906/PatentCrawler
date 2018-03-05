# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import re


def handle_item_group(item_group):
    """
    处理item_group函数
    :param item_group:
    :return:
    """
    AND = ' AND '
    OR = ' OR '
    NOT = ' NOT '
    exp_str = ""
    keyand = item_group.__getattribute__('And')
    keyor = item_group.__getattribute__('Or')
    keynot = item_group.__getattribute__('Not')
    if keyand is not None:
        parms = keyand.__getattribute__('parm')
        for parm in parms:
            exp_str += AND + parm
        exp_str = exp_str.replace(AND, '', 1)
    if keyor is not None:
        parms = keyor.__getattribute__('parm')
        for parm in parms:
            exp_str += OR + parm
        if keyand is None:
            exp_str = exp_str.replace(OR, '', 1)
    if keynot is not None:
        parms = keynot.__getattribute__('parm')
        for parm in parms:
            exp_str += NOT + parm
        if keyand is None and keyor is None:
            exp_str = exp_str.replace(NOT, '', 1)
    return exp_str


# 处理申请号的函数
def handle_number(title, request_number):
    word_reg = '[a-zA-Z]'
    if isinstance(request_number, ItemGroup):
        search_exp = handle_item_group(request_number)
        is_word = re.search(word_reg, search_exp[:2])
        if is_word is not None:
            return title + '=(' + search_exp + '+)'
        else:
            return title + '=(+' + search_exp + '+)'
    else:
        is_word = re.search(word_reg, request_number[:2])
        if is_word is not None:
            return title + '=(' + request_number + '+)'
        else:
            return title + '=(+' + request_number + '+)'


def handle_date_element(title, date_element):
    """
    处理日期元素的函数
    :param title:
    :param date_element:
    :return:
    """
    if isinstance(date_element, DateSelect):
        return title + date_element.__getattribute__('search_exp')
    else:
        raise Exception('We just support DateSelect for date element!')


def handle_invention_type(title, invention_type):
    """
    处理发明类型的函数
    :param title:
    :param invention_type:
    :return:
    """
    exp_str = ""
    if isinstance(invention_type, Or):
        OR = ' OR '
        keyor = invention_type
        if keyor is not None:
            parms = keyor.__getattribute__('parm')
            for parm in parms:
                if parm == 'I' or parm == 'U' or parm == 'D':
                    parm = '\"' + parm + '\"'
                elif parm.find('发明申请') != -1:
                    parm = '\"I\"'
                elif parm.find('实用新型') != -1:
                    parm = '\"U\"'
                elif parm.find('外观设计') != -1:
                    parm = '\"D\"'
                exp_str += OR + parm
            exp_str = exp_str.replace(OR, '', 1)
    elif isinstance(invention_type, str):
        if invention_type == 'I' or invention_type == 'U' or invention_type == 'D':
            exp_str = '\"' + invention_type + '\"'
        elif invention_type.find('发明申请') != -1:
            exp_str = '\"I\"'
        elif invention_type.find('实用新型') != -1:
            exp_str = '\"U\"'
        elif invention_type.find('外观设计') != -1:
            exp_str = '\"D\"'
    else:
        raise Exception('We just support string or Or for invention_type element!')
    return title + "=(" + exp_str + ")"


def default_handle(title, default):
    """
    默认处理函数
    :param title:
    :param default:
    :return:
    """
    if isinstance(default, ItemGroup):
        return title + '=(' + handle_item_group(default) + ')'
    elif isinstance(default, str):
        return title + '=(' + default + ')'
    else:
        raise Exception('We just support string or ItemGroup!')


def find_element_in_item_group(element, item_group):
    """
    在ItemGroup里面寻找相应的的element
    :param element:
    :param item_group:
    :return:
    """
    keyand = item_group.__getattribute__('And')
    keyor = item_group.__getattribute__('Or')
    keynot = item_group.__getattribute__('Not')
    if keyand is not None:
        parms = keyand.__getattribute__('parm')
        try:
            return parms.index(element)
        except:
            pass
    if keyor is not None:
        parms = keyor.__getattribute__('parm')
        try:
            return parms.index(element)
        except:
            pass
    if keynot is not None:
        parms = keynot.__getattribute__('parm')
        try:
            return parms.index(element)
        except:
            pass
    return None


title_case = {
    'request_number': handle_number,
    'request_date': handle_date_element,
    'publish_number': handle_number,
    'publish_date': handle_date_element,
    'invention_name': default_handle,
    'ipc_class_number': default_handle,
    'proposer': default_handle,
    'inventor': default_handle,
    'priority_number': default_handle,
    'priority_date': handle_date_element,
    'abstract': default_handle,
    'claim': default_handle,
    'instructions': default_handle,
    'key_word': default_handle,
    'locarno_class_number': default_handle,
    'description_of_the_design': default_handle,
    'agent': default_handle,
    'agency': default_handle,
    'proposer_post_code': default_handle,
    'proposer_address': default_handle,
    'proposer_location': default_handle,
    'FT_class_number': default_handle,
    'UC_class_number': default_handle,
    'ECLA_class_number': default_handle,
    'FI_class_number': default_handle,
    'English_invention_name': default_handle,
    'French_invention_name': default_handle,
    'German_invention_name': default_handle,
    'other_invention_name': default_handle,
    'English_abstract': default_handle,
    'PCT_enters_national_phase_date': handle_date_element,
    'PCT_international_application_number': handle_number,
    'French_abstract': default_handle,
    'German_abstract': default_handle,
    'other_abstract': default_handle,
    'PCT_international_application_date': handle_date_element,
    'PCT_international_publish_number': handle_number,
    'PCT_international_publish_date': handle_date_element,
    'CPC_class_number': default_handle,
    'C-SETS': default_handle,
    'invention_type': handle_invention_type,
    'publish_country': default_handle,
}
title_define = {
    'patent_id': '专利id',
    'request_number': '申请号',
    'request_date': '申请日',
    'publish_number': '公开（公告）号',
    'publish_date': '公开（公告）日',
    'invention_name': '发明名称',
    'ipc_class_number': 'IPC分类号',
    'proposer': '申请（专利权）人',
    'inventor': '发明人',
    'priority_number': '优先权号',
    'priority_date': '优先权日',
    'abstract': '摘要',
    'claim': '权利要求',
    'instructions': '说明书',
    'key_word': '关键词',
    'locarno_class_number': '外观设计洛迦诺分类号',
    'description_of_the_design': '外观设计简要说明',
    'agent': '代理人',
    'agency': '代理机构',
    'proposer_post_code': '申请人邮编',
    'proposer_address': '申请人地址',
    'proposer_location': '申请人所在国（省）',
    'FT_class_number': 'FT分类号',
    'UC_class_number': 'UC分类号',
    'ECLA_class_number': 'ECLA分类号',
    'FI_class_number': 'FI分类号',
    'English_invention_name': '发明名称（英）',
    'French_invention_name': '发明名称（法）',
    'German_invention_name': '发明名称（德）',
    'other_invention_name': '发明名称（其他）',
    'English_abstract': '摘要（英）',
    'PCT_enters_national_phase_date': 'PCT进入国家阶段日期',
    'PCT_international_application_number': 'PCT国际申请号',
    'French_abstract': '摘要（法）',
    'German_abstract': '摘要（德）',
    'other_abstract': '摘要（其他）',
    'PCT_international_application_date': 'PCT国际申请日期',
    'PCT_international_publish_number': 'PCT国际申请公开号',
    'PCT_international_publish_date': 'PCT国际申请公开日期',
    'CPC_class_number': 'CPC分类号',
    'C-SETS': 'C-SETS',
    'invention_type': '发明类型',
    'publish_country': '公开国',
    'legal_status': '法律状态',
    'legal_status_effective_date': '法律状态生效日'
}


# 日期选择器
class DateSelect:
    def __init__(self, select='=', date='2001-01-01', enddate=None):
        # 符号：'=', '>', '>=', '<', '<=', ':'
        self.select = select
        # 日期（固定格式）,eg: 2001-01-01
        self.date = date
        # 结束日期，当符号位为":"时，此变量有效，只从date开始到enddate结束
        self.enddate = enddate

        self.search_exp = ''
        if self.select != ':':
            self.search_exp = self.select + self.date
        else:
            self.search_exp = '=' + self.date + self.select + self.enddate

    def __repr__(self):
        return 'DateSelect{select=' + str(self.select) + ',date=' + str(self.date) + ',enddate=' + str(
            self.enddate) + '}'

    def __str__(self):
        return 'DateSelect{select=' + str(self.select) + ',date=' + str(self.date) + ',enddate=' + str(
            self.enddate) + '}'


class ItemGroup:
    def __init__(self, And=None, Or=None, Not=None):
        self.And = And
        self.Or = Or
        self.Not = Not

    def add_or(self, *parm):
        if self.Or is None:
            self.Or = Or(*parm)
        else:
            self.Or.add_parm(*parm)

    def __repr__(self):
        whole = ''
        if self.And is not None:
            whole += str(self.And)
        if self.Or is not None:
            whole += str(self.Or)
        if self.Not is not None:
            whole += str(self.Not)
        return whole


class And:
    def __init__(self, *parm):
        self.parm = list(parm)

    def add_parm(self, *ps):
        self.parm = self.parm + list(ps)

    def __repr__(self):
        andStr = ''
        for p in self.parm:
            andStr += str(p) + ';'
        return andStr


class Or:
    def __init__(self, *parm):
        self.parm = list(parm)

    def add_parm(self, *ps):
        self.parm = self.parm + ps

    def __repr__(self):
        andStr = ''
        for p in self.parm:
            andStr += str(p) + ';'
        return andStr


class Not:
    def __init__(self, *parm):
        self.parm = list(parm)

    def __repr__(self):
        andStr = ''
        for p in self.parm:
            andStr += str(p) + ';'
        return andStr


class SipoItem:
    """
    一个用来解析专利网站专利检索表达式的实例
    """

    def __init__(self, **kwargs):
        self.startIndex = 0
        self.__queryAnd = And()
        self.target_parm = {}  # 经过整理后的目标参数
        self.__prepare_item(kwargs)

        for title, value in title_define.items():
            key = kwargs.get(title)
            if key is not None:
                self.__queryAnd.add_parm(title_case.get(title)(value, key))
        self.__itemGroup = ItemGroup(And=self.__queryAnd)

        self.search_exp_cn = handle_item_group(self.__itemGroup)  # 生成的检索表达式
        self.target_parm = self.__check_target_parm(kwargs)

    def __prepare_item(self, items):
        invention_type = items.get('invention_type')
        if invention_type is not None:
            publish_country = items.get('publish_country')
            if publish_country is None:
                items['publish_country'] = 'CN'
            else:
                if isinstance(publish_country, str):
                    if publish_country != 'CN':
                        items['publish_country'] = ItemGroup(Or=Or(publish_country, 'CN'))
                elif isinstance(publish_country, ItemGroup):
                    if find_element_in_item_group('CN', publish_country) is None:
                        publish_country.add_or('CN')

    def __check_target_parm(self, parm):
        target = {}
        if isinstance(parm, dict):
            for key, value in parm.items():
                if key == 'invention_type':
                    if isinstance(value, Or):
                        for index, pvalue in enumerate(value.parm):
                            if pvalue == '"I"' or pvalue == '发明申请':
                                pvalue = {'en': '"I"', 'cn': '发明申请'}
                            elif pvalue == '"U"' or pvalue == '实用新型':
                                pvalue = {'en': '"U"', 'cn': '实用新型'}
                            elif pvalue == '"D"' or pvalue == '外观设计':
                                pvalue = {'en': '"D"', 'cn': '外观设计'}
                            else:
                                raise Exception('Please check the inventor_type')
                            value.parm[index] = pvalue
                    else:
                        if value == '"I"' or value == '发明申请':
                            value = {'en': '"I"', 'cn': '发明申请'}
                        elif value == '"U"' or value == '实用新型':
                            value = {'en': '"U"', 'cn': '实用新型'}
                        elif value == '"D"' or value == '外观设计':
                            value = {'en': '"D"', 'cn': '外观设计'}
                        else:
                            raise Exception('Please check the inventor_type')
                target[key] = value
        return target

    def __repr__(self):
        return self.search_exp_cn
