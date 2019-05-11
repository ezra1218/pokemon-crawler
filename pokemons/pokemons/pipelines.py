# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pokemons.settings import IMAGES_STORE
import os
import re

class PokemonsMongoPipeline(object):
    '''
    将数据存储至 MongoDB
    '''
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


class PokemonsImagesPipeline(ImagesPipeline):
    '''
    下载图片
    '''
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        '''
        当图片下载完成后调用该方法
        在这个方法中更改保存的文件名
        '''
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        
        # 更改保存的文件名
        filename = item['image_urls'][0].split('/')[-1]
        # 删除600px-、500px-
        filename = re.sub(r'\d{3}px-', '', filename)
        os.rename(IMAGES_STORE + results[0][1]['path'], IMAGES_STORE + filename)
        return item