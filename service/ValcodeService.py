# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
from PIL import Image
from pytesseract import image_to_string


class ValcodeService:
    def __initTable(self, threshold=140):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        return table

    # filepath要加后缀，可以是相对路径
    def getStringFromImage(self, filepath):
        im = Image.open(filepath)
        im = im.convert('L')
        binaryImage = im.point(self.__initTable(), '1')
        # binaryImage.show()
        valcode = image_to_string(binaryImage, config='-psm 7').strip()
        print(valcode)
        return valcode
