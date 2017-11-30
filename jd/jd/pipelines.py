# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from jd.settings import MONGODB_PORT,MONGDB_DB,MONGODB_DOC,MONGODB_HOST

# class JdPipeline(object):
#     def process_item(self, item, spider):
#         return item

class Write2JsonPipeline(object):
    def __init__(self):
        self.filename = open('jd.json','a',encoding='utf8')

    def process_item(self,item,spider):
        self.filename.write(json.dumps(dict(item),ensure_ascii=False)+"\n")
        return item

class write2MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGODB_HOST)
        db = self.client[MONGDB_DB]
        self.coll = db[MONGODB_DOC]

    def __del__(self):
        self.client.close()

    def process_item(self,item,spider):
        self.coll.insert(dict(item))
        return item