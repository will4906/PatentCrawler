"""
文件清理模块，调用后清理所有log和output文件
"""
import logging
import os
import sys

import shutil

from config.base_settings import OUTPUT_PATH

logging.getLogger(__name__).setLevel(logging.DEBUG)


def clean_outputs():
    """
    清理输出文件夹的内容
    :return:
    """
    output_list = os.listdir(OUTPUT_PATH)
    for output in output_list:
        shutil.rmtree(os.path.join(OUTPUT_PATH, output))


if __name__ == '__main__':
    clean_outputs()
