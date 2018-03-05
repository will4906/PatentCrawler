# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

url模块

使用者请勿修改此处内容，
开发者可根据实际需要自行定制开发
"""

# 首页，获取可以用来登录的ip地址
import requests

from config.query_config import QUERY_LIST

url_index = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'headers': {}
}

# 预处理地址，主要的目的是把ip发送给对面
url_pre_execute = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/preExecuteSearch!preExecuteSearch.do',
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://www.pss-system.gov.cn",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "X-Requested-With": "XMLHttpRequest"
    }
}

# 主查询地址
# 这个地址经常改变
url_search = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0712-executeCommandSearch.shtml',
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    'form_data': {
        "searchCondition.searchExp": '',
        "searchCondition.dbId": "VDB",
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.extendInfo['MODE']": "MODE_TABLE",
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        "searchCondition.originalLanguage": "",
        "searchCondition.targetLanguage": "",
        "wee.bizlog.modulelevel": "0200201",
        "resultPagination.limit": '12'
    }
}

# 翻页地址
url_page_turning = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml',
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    'form_data': {
        "resultPagination.limit": '12',
        "resultPagination.start": '',
        "resultPagination.totalCount": '',
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.dbId": "",
        "searchCondition.power": "false",
        "searchCondition.searchExp": '',
        "searchCondition.executableSearchExp": ''
    }
}
# 查询专利详情的地址
url_detail = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo-viewAbstractInfo.shtml',
    'form_data': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
        'wee.bizlog.modulelevel': '0201101'
    }
}

# cognation
url_related_info = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showPatentInfo-showPatentInfo.shtml',
    'headers': {},
    'form_data': {
        'literaInfo.nrdAn': '',
        'literaInfo.nrdPn': '',
        'literaInfo.fn': ''  # 这个参数不知道有啥用，不能没有但是可以为空
    }
}

# 验证码地址
url_captcha = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml',
    'headers': {}
}

# 登录地址
url_login = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check',
    'headers': {
        "Host": "www.pss-system.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Origin": "http://www.pss-system.gov.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8"
    },
    'form_data': {
        "j_loginsuccess_url": "",
        "j_validation_code": '',
        "j_username": '',
        "j_password": ''
    }
}

if __name__ == '__main__':
    search_exp_cn = QUERY_LIST[0].search_exp_cn
    form_data = url_search.get('formdata')
    form_data.__setitem__('searchCondition.searchExp', search_exp_cn)
    resp = requests.post(url_search.get('url'), headers=url_search.get('headers'), data=form_data)
    print(resp.content.decode())
