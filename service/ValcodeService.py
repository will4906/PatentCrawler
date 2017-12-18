# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import numpy as np
import os
import pickle

from PIL import Image


def split_letters(path):
    pix = np.array(Image.open(path).convert('L'))
    # threshold image
    pix = (pix > 135) * 255

    split_parts = [
        [7, 16],
        [20, 29],
        [33, 42],
        [46, 55]
    ]
    letters = []
    for part in split_parts:
        letter = pix[7:, part[0]: part[1]]
        letters.append(letter.reshape(9*13))
    return letters

class ValcodeService:

    # filepath要加后缀，可以是相对路径
    def getStringFromImage(self, filepath):
        letters = split_letters(filepath)
        with open('res/captcha/sipoknn.pkl', 'rb') as f:
            sipoknn = pickle.load(f)
            captcha = sipoknn.predict(letters)
            result = ''
            for cap in captcha:
                result += str(cap)
            print(result)
        return result
