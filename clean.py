"""
文件清理模块，调用后清理所有log和output文件
"""
import logging
import os

import shutil

from config.base_settings import OUTPUT_PATH, LOG_PATH

logging.getLogger(__name__).setLevel(logging.DEBUG)


def clean_outputs():
    """
    清理输出文件夹的内容
    :return:
    """
    output_list = os.listdir(OUTPUT_PATH)
    for output in output_list:
        shutil.rmtree(os.path.join(OUTPUT_PATH, output))


def clean_logs():
    """
    清理log文件夹的内容
    :return:
    """
    log_list = os.listdir(LOG_PATH)
    for log in log_list:
        try:
            os.remove(os.path.join(LOG_PATH, log))
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    clean_outputs()
    clean_logs()
