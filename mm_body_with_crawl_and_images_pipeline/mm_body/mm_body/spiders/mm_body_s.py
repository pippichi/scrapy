# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mm_body.items import MmBodyItem


class MmBodySSpider(CrawlSpider):
    name = 'mm_body_s'
    allowed_domains = ['tupianzj.com']
    start_urls = ['https://www.tupianzj.com/meinv/yishu/list_178_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+tupianzj.com/meinv/2\d{7}.+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath("//div[@class='warp']/div[@class='list_con bgff']/h1/text()").get()
        temp = title.rfind('(')
        if temp != -1 and title[-1] == ')':
            title = title[:temp]
        img = response.xpath("//div[@id='bigpic']/a[2]//img/@src").get()
        res = [img]
        item = MmBodyItem(title=title, image_urls=res)
        yield item
