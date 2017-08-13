# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from PIL import Image
from pytesseract import image_to_string

from service.LoginService import LoginService


def initTable(threshold=140):
 table = []
 for i in range(256):
     if i < threshold:
         table.append(0)
     else:
         table.append(1)

 return table

if __name__ == '__main__':
    LoginService({}).getALotValcode()
    for i in range(0,20):
        im = Image.open('valcode' + str(i) + '.png')
        im = im.convert('L')
        binaryImage = im.point(initTable(), '1')
        # binaryImage.show()
        print(image_to_string(binaryImage, config='-psm 7'))