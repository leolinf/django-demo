#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import requests
# import datetime
from pymongo import MongoClient
# from pyquery import PyQuery as pq


def crawler(url):
    while 1:
        try:
            html = requests.get(url, timeout=2).content
            break
        except:
            continue
  #  title = pq(html)('.article-title').text()
  #  content = pq(html)('.article-content').text()
    release_times = pq(html)('.item.time').text().replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
    if release_times == "":
        release_time = ''
    else:
        release_time = datetime.datetime.strptime(release_times, "%Y-%m-%d %H:%M:%S")
    author = pq(html)('.item.author').text()
    page_view = pq(html)('#js-read-times-text').text()
    db.data.update({"url":url}, {"$set":{"author":author}}, False, True)
    db.data.update({"url":url}, {"$set":{"page_view":page_view}}, False, True)
    db.data.update({"url":url}, {"$set":{"release_time":release_time}}, False, True)
    print page_view


conn = MongoClient('127.0.0.1', 27017)
db = conn.finance
for line in db.data.find():
    # data = json.loads(line)
    url = line['url']
    page_view = line['page_view']
    relationship = line['relationship']
    print url
    print page_view
    print relationship
    db.data.update({"url": url}, {"$set": {"page_view": int(page_view)}}, False, True)
    db.data.update({"url": url}, {"$set": {"relationship": int(relationship)}}, False, True)
