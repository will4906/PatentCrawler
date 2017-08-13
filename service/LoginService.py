# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import base64

import requests
from bs4 import BeautifulSoup

from config.LoginInfo import LoginInfo


class LoginService:
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
    checkUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check'
    codeurl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'

    def __init__(self, cookies):
        self.base64username = str(base64.b64encode(bytes(LoginInfo.USERNAME, encoding='utf-8')), 'utf-8')
        self.base64password = str(base64.b64encode(bytes(LoginInfo.PASSWORD, encoding='utf-8')), 'utf-8')
        self.valcode = ''
        self.loginData = {
        "j_loginsuccess_url": "",
        "j_validation_code": self.valcode,
        "j_username": self.base64username,
        "j_password": self.base64password
        }
        self.cookies = cookies

    def startLogin(self):
        valcode = requests.get(self.codeurl, cookies=self.cookies)
        f = open('valcode.png', 'wb')
        # 将response的二进制内容写入到文件中
        f.write(valcode.content)
        # 关闭文件流对象
        f.close()
        code = input('请输入验证码：')
        self.loginData["j_validation_code"] = str(code)
        resp = requests.post(self.checkUrl, headers=self.checkHeader, cookies=self.cookies,
                             data=self.loginData)
        soup = BeautifulSoup(resp.content, 'lxml')
        if str(soup.prettify()).find(LoginInfo.USERNAME + '，欢迎访问') != -1:
            print("登录成功")
            return True
        else:
            print('登录失败')
            return False

    def getALotValcode(self):
        for i in range(0,20):
            valcode = requests.get(self.codeurl, cookies=self.cookies)
            f = open('valcode' + str(i) + '.png', 'wb')
            # 将response的二进制内容写入到文件中
            f.write(valcode.content)
            # 关闭文件流对象
            f.close()