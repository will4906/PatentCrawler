# -*- coding: utf-8 -*-
"""
Created on 2017/5/11

@author: will4906
"""
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl Patent -s LOG_FILE=scrapy.log".split())
