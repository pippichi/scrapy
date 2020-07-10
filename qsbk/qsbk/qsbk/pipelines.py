# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class QsbkPipeline:
    def __init__(self):
        self.f = open(".duanzi.json", "wb")
        self.exporter = JsonLinesItemExporter(self.f, ensure_ascii=False, encoding="utf-8")

    def open_spider(self, spider):
        print("start")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.f.close()
        print("close spider")

