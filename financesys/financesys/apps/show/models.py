# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from mongoengine import Document, StringField, DateTimeField, IntField


class Data(Document):
    """抓取的华尔街的新闻数据"""
    # 标题
    title = StringField(max_length=200)
    # 内容
    content = StringField()
    # 发布时间
    time = DateTimeField()
    # 新闻相关程度
    relationship = IntField()
    # 新闻涉及区域
    date = DateTimeField()
    # 原网页
    url = StringField()
    # 发布时间
    release_time = DateTimeField()
    # 作者
    author = StringField()
    # 浏览量
    page_view = IntField()

    meta = {"colletion": "data",
            "index": [("release_time", 0)],
            }
