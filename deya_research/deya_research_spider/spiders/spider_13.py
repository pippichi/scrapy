import time
import re
from decimal import Decimal

import scrapy
import requests
import parsel
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider13(scrapy.Spider):
    """
    13.库存-生产企业-两油 指标爬虫
    """
    name = 'spider_13'
    allowed_domains = ['oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # 指标在数据库中的id
    index_id = 47

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '库存早报'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/text()").get()
        # 今日的日期会标记为红色，dom路径有所不同
        if date is None:
            date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/font/text()").get()

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
        p = response.css('#content > p::text').get()
        value = Decimal(re.search(r"(?<=两油库存)\d+(\.\d+)?", p).group())
        insert_value(date, value, self.index_id)


class Spider13History(scrapy.Spider):
    """
    13.库存-生产企业-两油 指标爬虫
    """
    name = 'spider_13_history'
    allowed_domains = ['oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # 指标在数据库中的id
    index_id = 47

    # 识别错误次数
    count = 0

    def start_requests(self):
        yield FormRequest(
            url=self.search_url,
            formdata={
                'pageNo': '1',
                'keyword': '库存早报'
            },
            callback=self.before_parse
        )

    def before_parse(self, response):
        lists = response.css('div.zixun.contentactive > ul.contentList > li')
        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        for li in lists:
            time.sleep(5)
            url = li.css('h2 > a::attr(href)').get()
            date = li.css('span.date::text').get()
            # 今日的日期会标记为红色，dom路径有所不同
            if date is None:
                date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']/font/text()").get()
            data = {
                'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
            }
            yield FormRequest(
                url=self.login_succeed_url,
                formdata=data,
                callback=self.parse,
                meta={'date': date},
                headers={
                    'Referer': self.search_url
                }
            )

        time.sleep(120)
        next_url = response.css('#simpledatatable_paginate > ul > li:nth-last-child(2) > a::attr(href)').get()
        next_page = re.search(r"(?<=goPage)\((\d)\)", next_url).group(1)
        if next_page is not None:
            yield FormRequest(
                url=self.search_url,
                formdata={
                    'pageNo': next_page,
                    'keyword': '库存早报'
                },
                callback=self.before_parse
            )

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        p = response.css('#content > p::text').get()
        value = Decimal(re.search(r"(?<=两油库存)\d+(\.\d+)?", p).group())
        insert_value(date, value, self.index_id)

