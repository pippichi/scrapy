# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request

class MmBodyPipeline:

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mm_body_images")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        img_urls = item['img_urls']
        for url in img_urls:
            img_name = url.split("/")[-1]
            request.urlretrieve(url, os.path.join(self.path, img_name))
        return item
