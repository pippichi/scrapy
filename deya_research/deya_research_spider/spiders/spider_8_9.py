#!/usr/bin/env python
# -*- encoding: utf-8 -*-   
# @Time    :  2020/8/6 下午4:39 
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


class Spider_8_9(scrapy.Spider):
    """
    8.供应-pp粉-产量-开工率 pp粉：开工率 以及
    9.供应-pp粉-国内产量-周度 pp粉：开工率指标爬虫
    """
    name = 'spider_8_9'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # pp粉：开工率指标id
    rate_index_id = 21
    # pp粉：国内产量：当周值指标id
    capacity_index_id = 22

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '聚丙烯粉料主要生产企业开工分析'}).text)
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
        # 开工率指标匹配
        sentence = response.xpath("//div[@id='content']//p/text()").extract_first()
        rate_value = Decimal(re.search(r"(?<=开工率)\d+(\.\d+)?", sentence).group())
        # 国内产量指标计算
        title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td//span/text()").getall()
        rows = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
        capacity_value = Decimal(0)
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
                rate_num = Decimal(rate.replace('%', '')) / 100
                capacity_value += capacity_num * rate_num
        capacity_value = (capacity_value / 52).quantize(Decimal('0'))
        insert_value(date, rate_value, self.rate_index_id)
        insert_value(date, capacity_value, self.capacity_index_id)