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


def image_as_array(image):
    image = np.asarray(image)
    image.flags['WRITEABLE'] = True
    return image


def convert_to_pure_black_white(image):
    width = image.shape[1]
    height = image.shape[0]
    image[0] = 255
    for line in image:
        line[0] = 255
        line[-1] = 255
    image[-1] = 255
    for w in range(width):
        for h in range(height):
            if image[h][w] < 237:
                image[h][w] = 0
            else:
                image[h][w] = 255
    image2 = image[:, 13:75]
    return image2


def split_letters(image):
    letters = [image[:, : 15], image[:, 15: 30], image[:, 30: 45], image[:, 45: 60]]
    return letters


def remove_noise_line(image):
    width = image.shape[1]
    height = image.shape[0]
    for w in range(width):
        count = 0
        for h in range(height):
            if image[h][w] < 100:
                count += 1
            else:
                if 2 > count > 0:
                    for c in range(count):
                        image[h - c - 1][w] = 255
                count = 0

    for h in range(height):
        count = 0
        for w in range(width):
            if image[h][w] < 100:
                count += 1
            else:
                if 2 > count > 0:
                    for c in range(count):
                        image[h][w - c - 1] = 255
                count = 0
    return image


def get_captcha_result(model_path, filename):
    """
    验证码解析
    :param model_path: 之前训练的模型位置
    :param filename: 需要解析的验证码全路径
    :return: 解析结果
    """
    image = np.asarray(Image.open(filename).convert('L'))
    image = (image > 135) * 255
    letters = [image[:, 6:18].reshape(20 * 12), image[:, 19:31].reshape(20 * 12), image[:, 33:45].reshape(20 * 12),
               image[:, 45:57].reshape(20 * 12)]
    model = joblib.load(model_path)
    result = ''
    for c in model.predict(letters):
        result += c
    return eval(result)


if __name__ == "__main__":
    for test in os.listdir('./test'):
        print(get_captcha_result('sipoknn.job', './test/' + test))
