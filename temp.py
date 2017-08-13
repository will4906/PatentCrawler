import json
import os

import simplejson as simplejson

from service.CookieService import CookieService


def saveCookies():
    f = open('temp_save/cookies.txt', 'w')
    # 将response的二进制内容写入到文件中
    f.write(str({
        'hello':'world',
        'good':'1'
    }))
    # 关闭文件流对象
    f.close()


def readCookies():
    if os.path.exists('temp_save/cookies.txt'):
        f = open('temp_save/cookies.txt', 'r')
        data = f.read()
        f.close()
        return data


if __name__ == '__main__':
    # CookieService.readCookies()
    # print(CookieService.getCookies())
    strkd = 'WEE_SID=u4vaicb7_q9VCQ9mDTN3RXAxHzN83o1KaBxsnn_4QDUY2BDmUXOF!-285926899!-304272566!1502610048763'
    print(strkd[8:])