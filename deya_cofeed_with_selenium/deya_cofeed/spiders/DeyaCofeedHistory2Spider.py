# -*- coding: utf-8 -*-
import math
import random
import time

import parsel
import requests
import scrapy
from scrapy import Request

from deya_cofeed.items import DeyaCofeedHistoryItem
from deya_cofeed.settings import DEFAULT_REQUEST_HEADERS
from deya_cofeed.tools import parse_title, parse_date, parse_total_records


class DeyaCofeedHistory2Spider(scrapy.Spider):
    name = 'deya_cofeed_history2_s'
    allowed_domains = ['www.cofeed.com']

    search_url = 'http://www.cofeed.com/history/index.asp?pagnum={pagnum}&time1={time1}&time2=0&keywords={keywords}'

    total_url = []

    time1 = ['2018/09/01', '2019/01/01']

    keywords = ['国内生猪及仔猪市场交易日报', '国内肉鸡市场交易日报']

    def start_requests(self):
        try:
            for t in self.time1:
                for k in self.keywords:
                    res = requests.get(url=self.search_url.format(pagnum=1, time1=t, keywords=k), headers=DEFAULT_REQUEST_HEADERS)
                    res = parsel.Selector(res.text)
                    total_records = res.xpath('//*[@id="page"]//text()').extract()[-1]
                    page = math.ceil(int(parse_total_records(total_records)) / 50)
                    time.sleep(5)
                    for i in range(page):
                        res = requests.get(url=self.search_url.format(pagnum=i+1, time1=t, keywords=k),
                                           headers=DEFAULT_REQUEST_HEADERS)
                        res = parsel.Selector(res.text)
                        channels = res.xpath('//*[@id="bean_left"]/div/div[3]')
                        urls = channels.xpath('.//a/@href').extract()
                        for u in urls:
                            self.total_url.append("http://www.cofeed.com" + u)
                        time.sleep(5)
            count = 0
            for i in self.total_url:
                if count % 3 == 0:
                    time.sleep(60 + int(random.uniform(10, 30)))
                yield Request(url=i, callback=self.parse)
                count += 1
        except Exception as e:
            print('!' * 30)
            print(e)
            print('!' * 30)

    def parse(self, response):
        try:
            res = []
            trs = response.xpath('//*[@id="infocontent"]/div//table[1]/tbody//tr')
            trs = response.xpath('//*[@id="infocontent"]//table[1]/tbody//tr') if len(trs) == 0 else trs

            for tr in trs:
                td = tr.xpath('count(.//td)').get()
                td_list = tr.xpath('.//td//text()').getall()
                while len(td_list) != int(td[0]):
                    td_list.append(" ")
                res.append(td_list)
            date = response.xpath('//*[@id="particular_con"]/div[2]/text()').get()
            title = response.xpath('//*[@id="particular_con"]/div[1]/text()').get()
            title = parse_title(title)
            date = parse_date(date)
            item = DeyaCofeedHistoryItem(content=res, date=date, title=title)
            yield item
        except Exception as e:
            print('!' * 30)
            print(e)
            print('!' * 30)
