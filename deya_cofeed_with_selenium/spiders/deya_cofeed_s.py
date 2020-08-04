# -*- coding: utf-8 -*-
import parsel
import scrapy
from scrapy import Request
import requests

from deya_cofeed.items import DeyaCofeedItem
from deya_cofeed.settings import DEFAULT_REQUEST_HEADERS


class DeyaCofeedSSpider(scrapy.Spider):
    name = 'deya_cofeed_s'
    allowed_domains = ['www.cofeed.com']

    search_url = ['https://www.cofeed.com/search.asp?keywords=国内生猪及仔猪市场交易日报',
                  'https://www.cofeed.com/search.asp?keywords=国内肉鸡市场交易日报']

    def start_requests(self):
        for su in self.search_url:
            res = requests.get(su, headers=DEFAULT_REQUEST_HEADERS)
            res = parsel.Selector(res.text)
            url = "http://www.cofeed.com" + res.xpath("//div[@class='channel_items']//a/@href").extract_first()

            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        res = []
        trs = response.xpath('//table[1]/tbody[1]/tr')
        for tr in trs:
            res.append(tr.xpath('.//td/text()').getall())
        item = DeyaCofeedItem(content=res)
        yield item
