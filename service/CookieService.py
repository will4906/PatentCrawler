import os

from config.BaseConfig import BaseConfig


class CookieService:

    cookies = {}

    @staticmethod
    def setCookies(co):
        CookieService.cookies = co

    @staticmethod
    def getCookies():
        return CookieService.cookies

    @staticmethod
    def saveCookies():
        f = open(BaseConfig.TEMP_DIR_NAME + '/cookies.txt', 'w')
        f.write(str(CookieService.cookies))
        f.close()

    @staticmethod
    def readCookies():
        if os.path.exists('temp_save/cookies.txt'):
            f = open('temp_save/cookies.txt', 'r')
            data = f.read()
            f.close()
            CookieService.cookies = eval(data)
            return True
        else:
            CookieService.cookies = {}
            return False

    @staticmethod
    def getCookiesFromList(coolist):
        for co in coolist:
            print('co' + str(co, encoding = "utf8"))
            if str(co, encoding = "utf8").find('WEE_SID') != -1:
                CookieService.cookies['WEE_SID'] = str(co, encoding = "utf8")[8:]
                print(str(co, encoding = "utf8")[8:])
                print(CookieService.cookies)
            elif str(co, encoding = "utf8").find('IS_LOGIN') != -1:
                CookieService.cookies['IS_LOGIN'] = str(co, encoding = "utf8")[9:]
                print(str(co, encoding = "utf8")[9:])
                print(CookieService.cookies)
            elif str(co, encoding = "utf8").find('JSESSIONID') != -1:
                CookieService.cookies['JSESSIONID'] = str(co, encoding = "utf8")[11:]
                print(str(co, encoding = "utf8")[11:])
                print(CookieService.cookies)
        print(CookieService.cookies)