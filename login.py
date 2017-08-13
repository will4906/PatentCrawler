import requests
import base64

from bs4 import BeautifulSoup

if __name__ == '__main__':
    checkHeader = {
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
    }
    header = {
        "Accept": "text / html, * / *;q = 0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }
    baseUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml'
    checkUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check'
    timeUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/checkLoginTimes-check.shtml'
    debugUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/sessionDeBugAC.do'
    codeurl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'

    '''此处改为大家在专利网注册的账号'''
    strName = 'iamcrawler2017'
    strPass = '1234567890hsh'


    base64Name = str(base64.b64encode(bytes(strName,encoding='utf-8')), 'utf-8')
    base64Pass = str(base64.b64encode(bytes(strPass,encoding='utf-8')), 'utf-8')
    timeData = {
        'username': strName
    }
    data = {
        "j_loginsuccess_url": "",
        "j_validation_code": "",
        "j_username": base64Name,
        "j_password": base64Pass
    }
    debugData = {
        "sessionDebugMod.opttype":"login",
        "sessionDebugMod.position":"keepalive",
        "sessionDebugMod.broswer":"Netscape5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "sessionDebugMod.userName":strName,
        "sessionDebugMod.cur_wee_sid":"",
        "sessionDebugMod.wee_sid":""
    }
    # base = requests.get(baseUrl, headers = header)
    # debugData["sessionDebugMod.cur_wee_sid"] = str(requests.utils.dict_from_cookiejar(base.cookies)['WEE_SID'])
    # debugData["sessionDebugMod.wee_sid"] = str(requests.utils.dict_from_cookiejar(base.cookies)['WEE_SID'])
    valcode = requests.get(codeurl)
    # valcode = requests.get(codeurl, headers=header, cookies=requests.utils.dict_from_cookiejar(base.cookies))
    f = open('valcode.png', 'wb')
    # 将response的二进制内容写入到文件中
    f.write(valcode.content)
    # 关闭文件流对象
    f.close()
    code = input('请输入验证码：')
    data["j_validation_code"] = str(code)
    # print(data)
    # timed = requests.post(timeUrl, headers = header, cookies = requests.utils.dict_from_cookiejar(base.cookies), data= timeData)
    # print(timed.content)
    # debugd = requests.post(debugUrl, headers = header, cookies = requests.utils.dict_from_cookiejar(base.cookies), data= debugData)
    # print(debugd.content)
    resp = requests.post(checkUrl, headers = checkHeader, cookies = requests.utils.dict_from_cookiejar(valcode.cookies), data=data)
    # print(resp.content)
    # resp = requests.get(checkUrl, cookies=requests.utils.dict_from_cookiejar(base.cookies))
    soup = BeautifulSoup(resp.content, 'lxml')
    # print(base.cookies)
    # print(resp.cookies)
    print(soup.prettify())