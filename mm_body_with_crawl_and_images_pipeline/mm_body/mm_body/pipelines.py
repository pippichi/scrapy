# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.images import ImagesPipeline

from mm_body import settings


class MmBodyPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        request_objs = super().get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super().file_path(request, response, info)
        path = path.replace("full/", "")
        title = request.item['title']
        base_path = settings.IMAGES_STORE
        temp_path = os.path.join(base_path, title)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        path = os.path.join(title, path)
        return path
