# -*- coding: utf-8 -*-
import parsel
import scrapy
from scrapy_splash import SplashRequest
import requests

from deya_cofeed.items import DeyaCofeedItem
from deya_cofeed.settings import DEFAULT_REQUEST_HEADERS


scripts = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(args.wait1))
  input = splash:select("#form-login > input[type=text]:nth-child(1)")
  input:send_text(args.user)
  js = "document.querySelector('#cofeed_PWD').value='dyzz8576'"
  splash:evaljs(js)
  input2 = splash:select('#cofeed_PWD')
  input2:send_text(args.password)
  assert(splash:wait(args.wait2))
  
  btn = splash:select('#form-login > input.btn')
  btn:mouse_click()
  assert(splash:wait(args.wait2))

  return splash:html()
end
"""


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

            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': scripts, 'wait1': 0.5, 'wait2': 4, 'user': "dyzz", 'password': "dyzz8576"})

    def parse(self, response):
        res = []
        trs = response.xpath('//table[1]/tbody[1]/tr')
        for tr in trs:
            res.append(tr.xpath('.//td/text()').getall())
        item = DeyaCofeedItem(content=res)
        yield item


