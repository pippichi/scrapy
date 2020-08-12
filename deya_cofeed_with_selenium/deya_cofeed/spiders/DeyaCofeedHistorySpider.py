# -*- coding: utf-8 -*-
import random
import time

import parsel
import scrapy
from scrapy import Request

from deya_cofeed.items import DeyaCofeedHistoryItem
from deya_cofeed.settings import DRIVER_PATH
from deya_cofeed.tools import parse_title, parse_date
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome


class DeyaCofeedHistorySpider(scrapy.Spider):
    name = 'deya_cofeed_history_s'
    allowed_domains = ['www.cofeed.com']

    search_url = ['https://www.cofeed.com/search.asp?keywords=国内生猪及仔猪市场交易日报',
                  'https://www.cofeed.com/search.asp?keywords=国内肉鸡市场交易日报']

    options = ChromeOptions()
    options.add_argument('-headless')
    options.add_argument("--no-sandbox")

    driver = Chrome(executable_path=DRIVER_PATH, chrome_options=options)

    total_url = []

    def start_requests(self):
        try:
            for su in self.search_url:
                self.driver.get(su)
                time.sleep(0.5)
                html = self.driver.page_source
                html_xpath = parsel.Selector(html)
                next_page = html_xpath.xpath('//*[@id="page"]/a[8]/@href').extract_first()
                if not next_page:
                    a_tag = self.driver.find_element_by_xpath('//*[@id="middle_right"]/div[1]/div[2]/div/a')
                    a_tag.click()
                    time.sleep(5)
                    html = self.driver.page_source
                    html_xpath = parsel.Selector(html)
                next_page = html_xpath.xpath('//*[@id="page"]/a[8]/@href').extract_first()
                while next_page and next_page != '':
                    url = ["http://www.cofeed.com" + r for r in
                           html_xpath.xpath("//div[@class='channel_items']//a/@href").extract()]
                    for u in url:
                        self.total_url.append(u)
                    next_page_btn = self.driver.find_element_by_xpath('//*[@id="page"]/a[8]')
                    next_page_btn.click()
                    time.sleep(6)
                    html = self.driver.page_source
                    html_xpath = parsel.Selector(html)
                    next_page = html_xpath.xpath('//*[@id="page"]/a[8]/@href').extract_first()
            self.driver.close()
            print("获取到了: " + str(len(self.total_url)) + " 条url")
            count = 0
            for _ in self.total_url:
                if count == len(self.total_url):
                    break
                if count % 3 == 0:
                    time.sleep(60 + int(random.uniform(10, 30)))
                yield Request(url=self.total_url[count], callback=self.parse)
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
