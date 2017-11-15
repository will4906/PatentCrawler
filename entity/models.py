# -*- coding: utf-8 -*-
"""
Created on 2017/3/19

@author: will4906
"""
import os
from peewee import SqliteDatabase, PrimaryKeyField, CharField, DateField, TextField, Model
from config.base_settings import  DATABASE_NAME


sqlite_db = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = sqlite_db


class Patents(BaseModel):

    # 行号
    row_id = PrimaryKeyField()
    # 专利id
    patent_id = CharField(unique=True)
    # 申请号
    request_number = CharField()
    # 申请日
    request_date = DateField()
    # 公开（公告）号
    publish_number = CharField()
    # 公开（公告）日
    publish_date = DateField()
    # 发明名称
    invention_name = CharField()
    # 申请（专利权）人
    proposer = CharField()
    # 发明人
    inventor = CharField()
    # 法律状态
    legal_status = CharField(null=True)
    #  法律状态生效日期
    legal_status_effective_date = DateField(null=True)
    # 摘要
    abstract = TextField(null=True)
    # IPC分类号
    ipc_class_number = CharField(null=True)
    # 优先权号
    priority_number = CharField(null=True)
    # 优先权日
    priority_date = DateField(null=True)
    # 外观设计洛迦诺分类号
    locarno_class_number = CharField(null=True)
    # 代理人
    agent = CharField(null=True)
    # 代理机构
    agency = CharField(null=True)
    # 申请人邮编
    proposer_post_code = CharField(null=True)
    # 申请人地址
    proposer_address = CharField(null=True)
    # 申请人所在国（省）
    proposer_location = CharField(null=True)
    # 发明类型
    invention_type = CharField(null=True)
    # 公开国
    publish_country = CharField(null=True)
    # 权利要求
    claim = CharField(null=True)
    # 说明书
    instructions = TextField(null=True)
    # FT分类号
    FT_class_number = CharField(null=True)
    # UC分类号
    UC_class_number = CharField(null=True)
    # ECLA分类号
    ECLA_class_number = CharField(null=True)
    # FI分类号
    FI_class_number = CharField(null=True)
    # CPC分类号
    CPC_class_number = CharField(null=True)