# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JianshuSSpider(CrawlSpider):
    name = 'jianshu_s'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        position_one = response.xpath("/html/body/div[1]/div[1]/div[1]/div[1]/section[1]")
        title = position_one.xpath(".//h1[1]/text()").get()
        avatar = position_one.xpath(".//div[1]/div[1]//img").get()
        print(avatar)
