import time
import re
from decimal import Decimal

import scrapy
import requests
import parsel
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider4(scrapy.Spider):
    """
    4.上游-产量-环氧丙烷-国内产量 指标爬虫
    """
    name = 'spider_4'
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
    index_id = 15

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '本周环氧丙烷开工率'}).text)
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
        p = response.css('#content > p:nth-child(9)::text').get()
        value = Decimal(re.search(r"(?<=产量)\d+(\.\d+)?", p).group())
        insert_value(date, value, self.index_id)


class Spider4History(scrapy.Spider):
    """
    4.上游-产量-环氧丙烷-国内产量 指标爬虫
    """
    name = 'spider_4_history'
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
    index_id = 15

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '本周环氧丙烷开工率'}).text)
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

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        p = response.css('#content > p:nth-child(9)::text').get()
        value = Decimal(re.search(r"(?<=产量)\d+(\.\d+)?", p).group())
        insert_value(date, value, self.index_id)
