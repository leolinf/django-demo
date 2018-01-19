# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoPipeline(object):

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_collection):

        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):

        settings = crawler.settings
        mongo_server = settings.get('MONGODB_SERVER', 'localhost')
        mongo_port = settings.get('MONGODB_PORT', 27017)
        mongo_db = settings.get('MONGODB_db', 'finance')
        mongo_collection = settings.get('MONGODB_collection', 'data')
        return cls(mongo_server, mongo_port, mongo_db, mongo_collection)

    def open_spider(self, spider):

        conn = pymongo.MongoClient(self.mongo_server, self.mongo_port)
        self.db = conn[self.mongo_db]

    def process_item(self, item, spider):

        item_data = dict(item)
        collect = self.mongo_collection
        collection = self.db[collect]
        collection.update({"url": item_data['url']}, {"$set": item_data}, True, True)
        return item
