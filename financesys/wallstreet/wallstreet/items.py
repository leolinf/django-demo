# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WallstreetItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = Field()
    # 内容
    content = Field()
    # 发布时间
    release_time = Field()
    # 新闻重要程度
    relationship = Field()
    # 新闻涉及区域
    area = Field()
    # 发布日期
    date = Field()
    # 发布时间
    time = Field()
    # 详情网页
    url = Field()
    # 浏览量
    page_view = Field()
    # 作者
    author = Field()
