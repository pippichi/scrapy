import re
import time
from decimal import Decimal

import requests
import scrapy


from deya_research_spider.tools import get_zc_cookie, insert_value


class Spider1Spider(scrapy.Spider):
    name = 'spider_1'
    allowed_domains = ['plas.chem99.com']
    sd_index_id = 12
    hd_index_id = 13
    search_url = "https://www.sci99.com/search/ajax.aspx"
    pageIndex = 1

    # 设置headers和cookies
    def start_requests(self):

        data = {
            'action': 'getlist',
            'keyword': 'pp粉料市场午间小结',
            'sccid': '686',
            'pageIndex': self.pageIndex,
            'siteids': '0',
            'orderby': 'true',

        }
        headers = {
            'referer': 'https://www.sci99.com/search',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        response = requests.post(self.search_url, data=data, headers=headers).json()

        hits = response[0]['hits']
        NewsKey = hits[0]['NewsKey']
        url = "http://plas.chem99.com/news/" + NewsKey + '.html'
        date = hits[0]['PubTime'].split('T')[0]

        # 获取cookie
        cookies = get_zc_cookie()
        yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        res = response.text
        a = re.findall('(\d+)-(\d+)元', str(res))
        sd_price = Decimal(a[-2][0])
        hd_price = Decimal(a[-1][0])
        insert_value(date, sd_price, self.sd_index_id)
        insert_value(date, hd_price, self.hd_index_id)



class Spider12SpiderHistory(scrapy.Spider):
    '''
    上游-价格-丙烯制品-pp粉-山东和华东 历史爬虫
    '''
    name = 'spider_1_2_history'
    allowed_domains = ['plas.chem99.com']
    sd_index_id = 12
    hd_index_id = 13
    search_url = "https://www.sci99.com/search/ajax.aspx"
    # 一共11页
    pageIndexs = [i for i in range(1, 11)]

    # 设置headers和cookies
    def start_requests(self):

        headers = {
            'referer': 'https://www.sci99.com/search',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

        # 获取cookie
        cookies = get_zc_cookie()

        for pageIndex in self.pageIndexs:
            data = {
                'action': 'getlist',
                'keyword': 'pp粉料市场午间小结',
                'sccid': '686',
                'pageIndex': pageIndex,
                'siteids': '0',
                'orderby': 'true',

            }

            response = requests.post(self.search_url, data=data, headers=headers).json()
            time.sleep(1)
            hits = response[0]['hits']
            for i in range(len(hits)):
                NewsKey = hits[i]['NewsKey']
                url = "http://plas.chem99.com/news/" + NewsKey + '.html'
                date = hits[i]['PubTime'].split('T')[0]
                time.sleep(2)

                yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        res = response.text
        a = re.findall('(\d+)-(\d+)元', str(res))
        sd_price = Decimal(a[-2][0])
        hd_price = Decimal(a[-1][0])
   

        insert_value(date, sd_price, self.sd_index_id)
        insert_value(date, hd_price, self.hd_index_id)