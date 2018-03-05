# -*- coding: utf-8 -*-
"""
Created on 2018/2/27

@author: will4906
"""
import sys

import click
from logbook import Logger, StreamHandler

StreamHandler(sys.stdout).push_application()
logger = Logger(__name__)


def init_log():
    click.echo('Log初始化完成')