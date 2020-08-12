#!/usr/bin/env python
# -*- encoding: utf-8 -*-   
# @Time    :  2020/8/6 下午3:54 
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


class Spider_7(scrapy.Spider):
    """
    7.上游-产量-丙烯-国内产量 丙烯：国内产量 指标爬虫
    """
    name = 'spider_7'
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
    index_id = 18

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '丙烯周度'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/text()").get()

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
        sentence = response.xpath("//div[@id='content']//p/text()").extract_first()
        value = Decimal(re.search(r"(?<=约)\d+(\.\d+)?", sentence).group())

        insert_value(date, value, self.index_id)


class Spider_7_History(scrapy.Spider):
    """
    7.上游-产量-丙烯-国内产量 丙烯：国内产量 指标历史数据爬虫
    """
    name = 'spider_7_history'
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
    index_id = 18

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '4', 'keyword': '丙烯周度产量统计'}).text)

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
        sentence = response.xpath("//div[@id='content']//p/text()").extract_first()
        value = Decimal(re.search(r"(?<=约)\d+(\.\d+)?", sentence).group())

        insert_value(date, value, self.index_id)