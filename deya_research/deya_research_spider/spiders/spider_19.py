import time
import re
from decimal import Decimal

import scrapy
import requests
import parsel
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider19North(scrapy.Spider):
    """
    19. PP出厂价：中石化：华北 指标爬虫
    """
    name = 'spider_19_1'
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
    index_id = 57

    factory_list = ['燕山', '齐鲁', '青岛', '济南']

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中石化华北PP'}).text)
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
        val = []
        tr = response.css('#content > table > tbody > tr')
        for i in tr:
            factory = i.css('td:first-child > p > span::text').get()
            if factory is not None and factory[0:2] in self.factory_list:
                val.append(i.css('td:nth-child(4) > p > span::text').get())
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19East(scrapy.Spider):
    """
    19. PP出厂价：中石化：华东 指标爬虫
    """
    name = 'spider_19_2'
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
    index_id = 58  # 华东

    factory_list = ['九江', '镇海']

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中石化华东PP'}).text)
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
        val = []
        tr = response.css('#content > table > tbody > tr')
        for i in tr:
            factory = i.css('td:first-child::text').get()
            if factory is not None and factory[0:2] in self.factory_list:
                if factory[0:2] == '九江':
                    val.append(int(i.css('td:nth-child(4)::text').get()) + 100)
                else:
                    val.append(int(i.css('td:nth-child(4)::text').get()))
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19South(scrapy.Spider):
    """
    19. PP出厂价：中石化：华南 指标爬虫
    """
    name = 'spider_19_3'
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
    index_id = 59  # 华南

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中石化华南PP'}).text)
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
        val = []
        tr = response.css('#content > table > tbody > tr')
        row_count = int(response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[1]/@rowspan').get())
        count_1 = 1
        tmp_1 = response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[2]/@rowspan').get()
        if tmp_1 is not None:
            count_1 = int(tmp_1)
        count_2 = 1
        tmp_2 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + 1 + 1)).get()
        if tmp_2 is not None:
            count_2 = int(tmp_2)
        count_3 = 1
        tmp_3 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + count_2 + 1 + 1)).get()
        if tmp_3 is not None:
            count_3 = int(tmp_3)
        count_4 = 1
        tmp_4 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + count_2 + count_3 + 1 + 1)).get()
        if tmp_4 is not None:
            count_4 = int(tmp_4)
        # 茂名石化
        for i in tr[1:count_1 + 1]:
            temp = i.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = i.css('td:nth-child(4) > p > span::text').get()
            val.append(temp)
        # 广州石化
        for j in tr[count_1 + 1:count_1 + count_2 + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            val.append(temp)
        # 福建联合
        for k in tr[count_1 + count_2 + 1: count_1 + count_2 + count_3 + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            if j.css('td:first-child > p > span::text').get() == 'HPPSS':
                continue
            val.append(temp)
        # 跳过海南炼厂
        for q in tr[count_1 + count_2 + count_3 + count_4 + 1: row_count + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            val.append(temp)
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19Middle(scrapy.Spider):
    """
    19. PP出厂价：中石化：华东中 指标爬虫
    """
    name = 'spider_19_4'
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
    index_id = 60  # 华东中

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中石化华中'}).text)
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
        val = []
        row_count = int(response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[1]/@rowspan').get())
        count = 1
        tr = response.css('#content > table > tbody > tr')
        for i in tr[1:row_count + 1]:
            company = i.xpath('td[1]/p/span/text()').get()
            if company[0:2] == '中天':
                tmp = i.xpath('td[1]/@rowspan').get()
                if tmp is not None:
                    count = int(tmp)
        for j in tr[1:row_count - count + 1]:
            temp = j.css('td:nth-child(3) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(4) > p > span::text').get()
            val.append(temp)
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19NorthHistory(scrapy.Spider):
    """
    19. PP出厂价：中石化：华北 指标爬虫
    """
    name = 'spider_19_1_history'
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
    index_id = 57

    factory_list = ['燕山', '齐鲁', '青岛', '济南']

    # 识别错误次数
    count = 0

    date_list = []

    def start_requests(self):
        pages = 20

        for i in range(16, pages + 1):
            time.sleep(30)
            yield FormRequest(
                url=self.search_url,
                formdata={
                    'pageNo': str(i),
                    'keyword': '[PP粒]：中石化华北PP'
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
                date = li.css("span.date > font::text").get()

            if date in self.date_list:
                continue

            self.date_list.append(date)

            data = {
                'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
            }
            yield FormRequest(
                url=self.login_succeed_url,
                formdata=data,
                headers={
                    'Referer': self.search_url
                },
                callback=self.parse,
                meta={'date': date}
            )

    # def start_requests(self):
    #     yield FormRequest(
    #         url=self.search_url,
    #         formdata={
    #             'pageNo': '1',
    #             'keyword': '[PP粒]：中石化华北PP'
    #         },
    #         callback=self.before_parse
    #     )
    #
    # def before_parse(self, response):
    #     lists = response.css('div.zixun.contentactive > ul.contentList > li')
    #
    #     temp = code_verify(self.img_url, self.code_verify_url)
    #     while temp.text != 'true':
    #         self.count += 1
    #         print("第{}次识别出错。".format(self.count))
    #         temp = code_verify(self.img_url, self.code_verify_url)
    #
    #     for li in lists:
    #         time.sleep(10)
    #         url = li.css('h2.title > a::attr(href)').get()
    #         date = li.css('span.date::text').get()
    #         # 今日的日期会标记为红色，dom路径有所不同
    #         if date is None:
    #             date = li.css("span.date > font::text").get()
    #
    #         if date in self.date_list:
    #             continue
    #
    #         self.date_list.append(date)
    #
    #         data = {
    #             'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
    #         }
    #         yield FormRequest(
    #             url=self.login_succeed_url,
    #             formdata=data,
    #             headers={
    #                 'Referer': self.search_url
    #             },
    #             callback=self.parse,
    #             meta={'date': date}
    #         )
    #
    #     time.sleep(60)
    #     next_url = response.css('#simpledatatable_paginate > ul > li:nth-last-child(2) > a::attr(href)').get()
    #     next_page = re.search(r"(?<=goPage)\((\d)\)", next_url).group(1)
    #     if next_page is not None:
    #         yield FormRequest(
    #             url=self.search_url,
    #             formdata={
    #                 'pageNo': next_page,
    #                 'keyword': '[PP粒]：中石化华北PP'
    #             },
    #             callback=self.before_parse
    #         )

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        val = []
        tr = response.css('#content > table > tbody > tr')
        for i in tr:
            factory = i.css('td:first-child > p > span::text').get()
            if factory is not None and factory[0:2] in self.factory_list:
                val.append(i.css('td:nth-child(4) > p > span::text').get())
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19EastHistory(scrapy.Spider):
    """
    19. PP出厂价：中石化：华东 指标爬虫
    """
    name = 'spider_19_2_history'
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
    index_id = 58  # 华东

    factory_list = ['九江', '镇海']

    # 识别错误次数
    count = 0

    def start_requests(self):
        pages = 2

        for i in range(1, pages + 1):
            time.sleep(60)
            yield FormRequest(
                url=self.search_url,
                formdata={
                    'pageNo': str(i),
                    'keyword': '[PP粒]：中石化华东PP'
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

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        val = []
        tr = response.css('#content > table > tbody > tr')
        for i in tr:
            factory = i.css('td:first-child::text').get()
            if factory is not None and factory[0:2] in self.factory_list:
                if factory[0:2] == '九江':
                    val.append(int(i.css('td:nth-child(4)::text').get()) + 100)
                else:
                    val.append(int(i.css('td:nth-child(4)::text').get()))
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19SouthHistory(scrapy.Spider):
    """
    19. PP出厂价：中石化：华南 指标爬虫
    """
    name = 'spider_19_3_history'
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
    index_id = 59  # 华南

    # 识别错误次数
    count = 0

    def start_requests(self):
        pages = 2

        for i in range(1, pages + 1):
            time.sleep(60)
            yield FormRequest(
                url=self.search_url,
                formdata={
                    'pageNo': str(i),
                    'keyword': '[PP粒]：中石化华南PP'
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

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        val = []
        tr = response.css('#content > table > tbody > tr')
        row_count = int(response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[1]/@rowspan').get())
        count_1 = 1
        tmp_1 = response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[2]/@rowspan').get()
        if tmp_1 is not None:
            count_1 = int(tmp_1)
        count_2 = 1
        tmp_2 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + 1 + 1)).get()
        if tmp_2 is not None:
            count_2 = int(tmp_2)
        count_3 = 1
        tmp_3 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + count_2 + 1 + 1)).get()
        if tmp_3 is not None:
            count_3 = int(tmp_3)
        count_4 = 1
        tmp_4 = response.xpath('//*[@id="content"]/table/tbody/tr[{}]/td[1]/@rowspan'
                               .format(count_1 + count_2 + count_3 + 1 + 1)).get()
        if tmp_4 is not None:
            count_4 = int(tmp_4)
        # 茂名石化
        for i in tr[1:count_1 + 1]:
            temp = i.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = i.css('td:nth-child(4) > p > span::text').get()
            val.append(temp)
        # 广州石化
        for j in tr[count_1 + 1:count_1 + count_2 + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            val.append(temp)
        # 福建联合
        for k in tr[count_1 + count_2 + 1: count_1 + count_2 + count_3 + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            if j.css('td:first-child > p > span::text').get() == 'HPPSS':
                continue
            val.append(temp)
        # 跳过海南炼厂
        for q in tr[count_1 + count_2 + count_3 + count_4 + 1: row_count + 1]:
            temp = j.css('td:nth-child(2) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(3) > p > span::text').get()
            val.append(temp)
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)


class Spider19MiddleHistory(scrapy.Spider):
    """
    19. PP出厂价：中石化：华东中 指标爬虫
    """
    name = 'spider_19_4_history'
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
    index_id = 60  # 华东中

    # 识别错误次数
    count = 0

    def start_requests(self):
        pages = 2

        for i in range(1, pages + 1):
            time.sleep(60)
            yield FormRequest(
                url=self.search_url,
                formdata={
                    'pageNo': str(i),
                    'keyword': '[PP粒]：中石化华中'
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

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        val = []
        row_count = int(response.xpath('//*[@id="content"]/table/tbody/tr[2]/td[1]/@rowspan').get())
        count = 1
        tr = response.css('#content > table > tbody > tr')
        for i in tr[1:row_count + 1]:
            company = i.xpath('td[1]/p/span/text()').get()
            if company[0:2] == '中天':
                tmp = i.xpath('td[1]/@rowspan').get()
                if tmp is not None:
                    count = int(tmp)
        for j in tr[1:row_count - count + 1]:
            temp = j.css('td:nth-child(3) > p > span::text').get()
            if re.fullmatch(r'\d*', temp) is None:
                temp = j.css('td:nth-child(4) > p > span::text').get()
            val.append(temp)
        value = Decimal(min(val))
        insert_value(date, value, self.index_id)