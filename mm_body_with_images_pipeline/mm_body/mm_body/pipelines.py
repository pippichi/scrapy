# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.images import ImagesPipeline

from mm_body import settings


class MmBodyPipeline:
    def process_item(self, item, spider):
        return item

class MMBodyPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用
        # 其实这个方法本身就是去发送下在请求的
        request_objs = super().get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super().file_path(request, response, info)
        path = path.replace("full/", "")
        category = request.item.get("category", "my_category")
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store, category)
        if not category_path:
            os.mkdir(category_path)
        path = os.path.join(category, path)
        return path
