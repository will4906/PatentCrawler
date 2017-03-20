# -*- coding: utf-8 -*-
"""
Created on 2017/3/20

@author: will4906
"""


# str = "//*[@id=\"search_result\"]/div[4]/div[1]/ul/li[4]/div/div[1]/h1/div[2]/a/b"
strLeft = "//*[@id=\"search_result\"]/div[4]/div[1]/ul/li["
strRight = "]/div/div[1]/h1/div[2]/a/b"

for index in range(1,13):
    print(strLeft + str(index) + strRight)