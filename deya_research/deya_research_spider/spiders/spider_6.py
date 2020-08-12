#!/usr/bin/env python
# -*- encoding: utf-8 -*-   
# @Time    :  2020/8/6 下午2:58 
# @Author  :  TCL
import re
import time
from datetime import datetime
from decimal import Decimal

import parsel
import pymysql
import requests
import scrapy
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider_6(scrapy.Spider):
    """
    6.上游-产量-丙烯酸-国内产量 指标爬虫
    """
    name = 'spider_6'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # 指标在数据库中的id
    index_id = 17

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '丙烯酸及丁酯'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/text()").get()
        # 今日的日期会标记为红色，dom路径有所不同
        if date is None:
            response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/font/text()").get()

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        data = {
            'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
        }

        yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td//span/text()").getall()
        rows = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
        value = Decimal(0)
        for row in rows:
            data = parsel.Selector(row).xpath("//td").extract()
            if len(data) == len(title):
                index1, index2 = 2, 3
            else:
                index1, index2 = 1, 2
            capacity = parsel.Selector(data[index1]).xpath("//span/text()").extract_first()
            rate = parsel.Selector(data[index2]).xpath("//span/text()").extract_first()
            if capacity is None or rate is None:
                continue
            else:
                capacity_num = Decimal(capacity)
                rate_num = Decimal(rate[:-1]) / 100
                value += capacity_num * rate_num
        value = (value / 52).quantize(Decimal('0'))

        insert_value(date, value, self.index_id)

class Spider_6_History(scrapy.Spider):
    """
    6.上游-产量-丙烯酸-国内产量 历史指标数据爬虫
    """
    name = 'spider_6_history'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # 指标在数据库中的id
    index_id = 17

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '12', 'keyword': '丙烯酸及丁酯产品装置'}).text)
        items = response.xpath("//div[@class='zixun contentactive']//ul[@class='contentList']/li").getall()

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        for item in items:
            time.sleep(2)
            url = parsel.Selector(item).xpath("//h2//a/@href").get()
            date = parsel.Selector(item).xpath("//span[@class='date']/text()").get()
            # 今日的日期会标记为红色，dom路径有所不同
            if date is None:
                date = parsel.Selector(item).xpath("//span[@class='date']/font/text()").get()
            data = {
                'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
            }

            yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td//span/text()").getall()
        if len(title) == 0:
            title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td//strong/text()").getall()
        rows = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
        value = Decimal(0)
        for row in rows:
            data = parsel.Selector(row).xpath("//td").extract()
            if len(data) == len(title):
                index1, index2 = 2, 3
            else:
                index1, index2 = 1, 2
            capacity = parsel.Selector(data[index1]).xpath("//span/text()").extract_first()
            if capacity is None:
                capacity = parsel.Selector(data[index1]).xpath("//text()").extract_first()
            if capacity is None:
                capacity = parsel.Selector(data[index1]).xpath("//p/text()").extract_first()

            rate = parsel.Selector(data[index2]).xpath("//span/text()").extract_first()
            if rate is None:
                rate = parsel.Selector(data[index2]).xpath("//text()").extract_first()
            if rate is None:
                rate = parsel.Selector(data[index2]).xpath("//p/text()").extract_first()
            if capacity is None or rate is None:
                continue
            else:
                capacity_num = Decimal(capacity)
                rate_num = Decimal(rate.replace('%', '')) / 100
                value += capacity_num * rate_num
        value = (value / 52).quantize(Decimal('0'))

        insert_value(date, value, self.index_id)