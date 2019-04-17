# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class PokemonsPipeline(object):

    def __init__(self):
        # 建立与数据库的链接
        self.conn = MongoClient(host='localhost', port=27017)
        # 创建数据库
        db = self.conn['POKEMONS_STATS']
        self.collection = db['STATS']

    def process_item(self, item, spider):
        # 将爬取到的数据插入数据库
        self.collection.insert_one(dict(item))
        return item
