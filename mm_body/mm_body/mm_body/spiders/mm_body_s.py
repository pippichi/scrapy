# -*- coding: utf-8 -*-
import scrapy

from items import MmBodyItem


class MmBodySSpider(scrapy.Spider):
    name = 'mm_body_s'
    allowed_domains = ['tupianzj.com']
    start_urls = ['https://www.tupianzj.com/meinv/yishu/list_178_1.html']
    base_url = 'https://www.tupianzj.com/meinv/yishu/list_178_{page}.html'

    def parse(self, response):
        ul = response.xpath("//ul[@class='list_con_box_ul']/li/a/img/@src|//ul[@class='list_con_hot_ul']/li/a/img/@src").getall()
        # for li in ul:
        #     # 自动添加https://头部
        #     li = response.urljoin(li)
        #     print(li)
        # response.urljoin自动添加https://头部
        urls = list(map(lambda url: response.urljoin(url), ul))
        print(urls)
        items = MmBodyItem(img_urls=urls)
        yield items
