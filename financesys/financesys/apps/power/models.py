# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from mongoengine import Document, StringField, IntField,\
    DateTimeField

# Create your models here.


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


class User(AbstractUser):
    '''用户模型'''
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username
