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

url_index = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'headers': {}
}

# 预处理地址，主要的目的是把ip发送给对面
url_pre_execute = {
    # 'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/preExecuteSearch!preExecuteSearch.do',
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/pageIsUesd-pageUsed.shtml',
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
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0402-executeCommandSearch.shtml',
    # 'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0712-executeCommandSearch.shtml',
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    },
    'form_data': {
        "searchCondition.searchExp": '',
        "searchCondition.dbId": "VDB",
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.extendInfo['MODE']": "MODE_TABLE",
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        "searchCondition.originalLanguage": "",
        "searchCondition.targetLanguage": "",
        "wee.bizlog.modulelevel": '0200201',
        "resultPagination.limit": '12'
    },
    'crawler_id': '0'
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
    },
    'crawler_id': '0'
}
# 查询专利详情的地址
url_detail = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo0404-viewAbstractInfo.shtml',
    'form_data': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
        'wee.bizlog.modulelevel': '0201101'
    },
    'headers': {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.pss-system.gov.cn',
        'Origin': 'http://www.pss-system.gov.cn',
        'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    },
    'crawler_id': '1'
}

# cognation
url_related_info = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showPatentInfo0405-showPatentInfo.shtml',
    'headers': {},
    'form_data': {
        'literaInfo.nrdAn': '',
        'literaInfo.nrdPn': '',
        'literaInfo.fn': ''  # 这个参数不知道有啥用，不能没有但是可以为空
    },
    'crawler_id': '2'
}

# full text
url_full_text = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showFullText0406-viewFullText.shtml',
    'headers': {},
    'form_data': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
    },
    'crawler_id': '3'
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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.pss-system.gov.cn',
        'Origin': 'http://www.pss-system.gov.cn',
        'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    },
    'form_data': {
        "j_loginsuccess_url": "",
        "j_validation_code": '',
        "j_username": '',
        "j_password": ''
    }
}

if __name__ == '__main__':
    resp = requests.get(url_index.get('url'), headers=url_search.get('headers'))
    coo = resp.cookies
    print(coo)
    coo.__delitem__('JSESSIONID')
    coo.set('JSESSIONID', '8U9nCtA0LoRYs75ado1-eMcbTsLZINYi2r3aILoqbKjmy9DbWY_v!891074563!-395222046',
            domain='www.pss-system.gov.cn')
    coo.__delitem__('IS_LOGIN')
    coo.set('IS_LOGIN', 'true', domain='www.pss-system.gov.cn/sipopublicsearch/patentsearch')
    coo.__delitem__("WEE_SID")
    coo.set("WEE_SID", '8U9nCtA0LoRYs75ado1-eMcbTsLZINYi2r3aILoqbKjmy9DbWY_v!891074563!-395222046!1522147184692',
            domain='www.pss-system.gov.cn/sipopublicsearch/patentsearch')
    print(coo)
    form_data = url_detail.get('form_data')
    # '''
    # 'nrdAn': '',
    #     'cid': '',
    #     'sid': '',
    #     'wee.bizlog.modulelevel': '0201101'
    # '''
    form_data.__setitem__('nrdAn', 'CN201711283836')
    form_data.__setitem__('cid', 'CN201711283836.720180302FM')
    form_data.__setitem__('sid', 'CN201711283836.720180302FM')
    resp = requests.post(url_detail.get('url'), headers=url_detail.get('headers'), cookies=coo, data=form_data)
    print(resp.text)
    pass
    # search_exp_cn = QUERY_LIST[0].search_exp_cn
    # form_data = url_search.get('formdata')
    # form_data.__setitem__('searchCondition.searchExp', search_exp_cn)

    # print(resp.content.decode())
