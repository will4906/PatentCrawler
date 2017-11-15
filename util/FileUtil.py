# -*- coding: utf-8 -*-
"""
Created on 2017/4/1

@author: will4906
"""


class FileUtil:
    def __init__(self, filename, mode):
        self.__filename = filename
        self.__file = open(self.__filename, mode, encoding='utf8')

    def __del__(self):
        self.__file.close()

    def writeLine(self, strLine):
        self.__file.write(strLine + "\n")
        self.__file.flush()

