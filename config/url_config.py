# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""

# 首页，获取可以用来登录的ip地址
index = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'headers': {}
}

# 预处理地址，主要的目的是把ip发送给对面
preExecute = {
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
mainSearch = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0712-executeCommandSearch.shtml',
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    'formdata': {
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

pageTurning = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml',
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    'formdata': {
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
detailSearch = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo-viewAbstractInfo.shtml',
    'formdata': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
        'wee.bizlog.modulelevel': '0201101'
    }
}

# cognation
relatedInfo = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showPatentInfo-showPatentInfo.shtml',
    'headers': {},
    'formdata': {
        'literaInfo.nrdAn': '',
        'literaInfo.nrdPn': '',
        'literaInfo.fn': ''                     # 这个参数不知道有啥用，不能没有但是可以为空
    }
}