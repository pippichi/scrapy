import re
import time
from decimal import Decimal

import parsel
import requests
import scrapy
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider10Spider(scrapy.Spider):
    '''
    10：供应-pp粉-产量-国内产量（当月）
    '''
    name = 'spider_10'
    allowed_domains = ['news.oilchem.net']

    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 23

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': 'PP粉料产量统计'}).text)
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
        production_value = Decimal(re.findall(r"产量为(\d+\.\d+?)万吨", sentence)[0])
        insert_value(date, production_value, self.index_id)


class Spider10SpiderHistory(scrapy.Spider):
    '''
    10：历史爬虫
    供应-pp粉-产量-国内产量（当月）
    '''
    name = 'spider_10_history'
    allowed_domains = ['news.oilchem.net']

    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 23

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': 'PP粉料产量统计'}).text)
        items = response.xpath("//ul[@class='contentList']/li").getall()

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        for item in items:
            time.sleep(2)
            url = parsel.Selector(item).xpath("//h2//a/@href").get()
            date = parsel.Selector(item).xpath("//span[@class='date']//text()").get()
            data = {
                'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
            }
            yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        sentence = response.xpath("//div[@id='content']//p/text()").extract_first()
        production_value = Decimal(re.findall(r"产量为(\d+\.\d+?)万吨", sentence)[0])
        insert_value(date, production_value, self.index_id)