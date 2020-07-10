# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from wxapp.wxapp.items import WxappItem


class WxappSpiderSpider(scrapy.Spider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    base_domain = "http://www.wxapp-union.com/"
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=1&page=1']


    def parse(self, response):
        url = response.xpath("//div[@class='list_new Framebox cl']//h3[@class='list_title']/a/@href").getall()
        print(url)
        for u in url:
            yield Request(self.base_domain+u, callback=self.parse_next)
        next_url = response.xpath("//div[@class='pgs cl']/div[@class='pg']//a[last()]/@href").get()
        yield Request(next_url, callback=self.parse)

    def parse_next(self, response):
        base = response.xpath("//div[@class='h hm cl']//p[@class='authors']")
        author = base.xpath(".//a/text()").get()
        item = WxappItem(author=author)
        yield item
