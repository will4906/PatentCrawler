# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906

验证码解析模块
"""
import numpy as np
import os

from PIL import Image
from sklearn.externals import joblib


def split_letters(path):
    """
    字符分割
    :param path:
    :return:
    """
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


def get_captcha_result(model_path, filename):
    """
    验证码解析
    :param model_path: 之前训练的模型位置
    :param filename: 需要解析的验证码全路径
    :return: 解析结果
    """
    sipo_knn = joblib.load(model_path)
    letters = split_letters(filename)
    result = ''
    for r in sipo_knn.predict(letters):
        result += str(r)
    return result


if __name__ == "__main__":
    for test in os.listdir('./test'):
        print(get_captcha_result('sipoknn.job', './test/' + test))
