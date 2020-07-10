# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from qsbk.qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    base_domain = "https://www.qiushibaike.com"
    start_urls = ['http://qiushibaike.com/text/page/1/']

    def parse(self, response):
        # selectlist
        contentLeft = response.xpath("//div[@class='col1 old-style-col1']/div")
        for c in contentLeft:
            # selector
            content = c.xpath(".//a[@class='contentHref']/div/span//text()").getall()
            # duanzi = {"content": content}
            item = QsbkItem(content=content)
            yield item

        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return 
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)_ 
        
