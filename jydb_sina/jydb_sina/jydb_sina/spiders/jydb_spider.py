# -*- coding: utf-8 -*-
import scrapy


class JydbSpiderSpider(scrapy.Spider):
    name = 'jydb_spider'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn/search/mblog?hideSearchFrame=&keyword=胶原蛋白&page=1']

    def parse(self, response):
        print(response.text)
