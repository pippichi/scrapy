# -*- coding: utf-8 -*-
import scrapy


class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['http://car.autohome.com.cn/']

    def parse(self, response):
        pass
