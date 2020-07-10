# -*- coding: utf-8 -*-
import scrapy

from mm_body.items import MmBodyItem


class MmBodySSpider(scrapy.Spider):
    name = 'mm_body_s'
    allowed_domains = ['tupianzj.com']
    start_urls = ['https://www.tupianzj.com/meinv/yishu/list_178_1.html']

    def parse(self, response):
        urls = response.xpath("//ul[@class='list_con_box_ul']/li/a/img/@src|//ul[@class='list_con_hot_ul']/li/a/img/@src").getall()
        urls = map(lambda x: response.urljoin(x), urls)
        item = MmBodyItem(image_urls=urls)
        yield item
