import time
import re
from decimal import Decimal

import scrapy
import requests
import parsel
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider14(scrapy.Spider):
    """
    14.	库存-生产企业-拉丝级
        库存-生产企业-纤维级
        库存-生产企业-贸易商环比
        库存-下游企业-塑编环比
        库存-生产企业-BOPP环比 指标爬虫
    """
    name = 'spider_14'
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
    draw_index_id = 52   # 拉丝
    fiber_index_id = 53   # 纤维
    merchant_index_id = 54   # 贸易商
    plastic_woven_index_id = 55   # 塑编
    bopp_index_id = 56   # BOPP

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': 'PP周度库存'}).text)
        url = response.xpath("//ul[@class='contentList']/li[2]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[2]//span[@class='date']/text()").get()
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
        draw_p = response.css('#content > p:nth-child(24) > span::text').get()
        fiber_p = response.css('#content > p:nth-child(25) > span::text').get()
        merchant_p = response.css('#content > p:nth-child(31) > span::text').get()
        plastic_woven_p = response.css('#content > p:nth-child(48) > span::text').get().replace(" ", "")
        bopp_p = response.css('#content > p:nth-child(54) > span::text').get()
        draw_value = Decimal(re.search(r"(?<=企业库存在)\d+(\.\d+)?", draw_p).group())
        fiber_value = Decimal(re.search(r"(?<=企业库存在)\d+(\.\d+)?", fiber_p).group())

        merchant_re = re.search(r"(?<=贸易商库存较上周增加)\d+(\.\d+)?", merchant_p)
        if merchant_re:
            merchant_value = Decimal(merchant_re.group())
        else:
            merchant_value = -Decimal(re.search(r"(?<=贸易商库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", merchant_p).group())

        plastic_woven_re = re.search(r"(?<=原料库存天数较上周上涨)\d+(\.\d+)?", plastic_woven_p)
        if plastic_woven_re:
            plastic_woven_value = Decimal(plastic_woven_re.group())
        else:
            plastic_woven_value = -Decimal(re.search(r"(?<=原料库存天数较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", plastic_woven_p).group())

        bopp_re = re.search(r"(?<=BOPP原料库存较上周上涨)\d+(\.\d+)?", bopp_p)
        if bopp_re:
            bopp_value = Decimal(bopp_re.group())
        else:
            bopp_value = -Decimal(re.search(r"(?<=BOPP原料库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", bopp_p).group())
        insert_value(date, draw_value, self.draw_index_id)
        insert_value(date, fiber_value, self.fiber_index_id)
        insert_value(date, merchant_value, self.merchant_index_id)
        insert_value(date, plastic_woven_value, self.plastic_woven_index_id)
        insert_value(date, bopp_value, self.bopp_index_id)


class Spider14History(scrapy.Spider):
    """
    14.	库存-生产企业-拉丝级
        库存-生产企业-纤维级
        库存-生产企业-贸易商环比
        库存-下游企业-塑编环比
        库存-生产企业-BOPP环比 指标爬虫
    """
    name = 'spider_14_history'
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
    draw_index_id = 52  # 拉丝
    fiber_index_id = 53  # 纤维
    merchant_index_id = 54  # 贸易商
    plastic_woven_index_id = 55  # 塑编
    bopp_index_id = 56  # BOPP

    # 识别错误次数
    count = 0

    def start_requests(self):
        yield FormRequest(
            url=self.search_url,
            formdata={
                'pageNo': '4',
                'keyword': 'PP周度库存'
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

        # time.sleep(120)
        # next_url = response.css('#simpledatatable_paginate > ul > li:nth-last-child(2) > a::attr(href)').get()
        # next_page = re.search(r"(?<=goPage)\((\d)\)", next_url).group(1)
        # if next_page is not None:
        #     yield FormRequest(
        #         url=self.search_url,
        #         formdata={
        #             'pageNo': next_page,
        #             'keyword': 'PP周度库存'
        #         },
        #         callback=self.before_parse
        #     )

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        draw_p = response.css('#content > p:nth-child(24) > span::text').get()
        draw_re = re.search(r"(?<=企业库存在)\d+(\.\d+)?", draw_p)
        if draw_re is not None:
            fiber_p = response.css('#content > p:nth-child(25) > span::text').get()
            fiber_re = re.search(r"(?<=企业库存在)\d+(\.\d+)?", fiber_p)
            draw_value = Decimal(draw_re.group())
            fiber_value = Decimal(fiber_re.group())
            insert_value(date, draw_value, self.draw_index_id)
            insert_value(date, fiber_value, self.fiber_index_id)

            merchant_p = response.css('#content > p:nth-child(31) > span::text').get()
            plastic_woven_p = response.css('#content > p:nth-child(48) > span::text').get().replace(" ", "")
            bopp_p = response.css('#content > p:nth-child(54) > span::text').get()

            merchant_re = re.search(r"(?<=贸易商库存较上周增加)\d+(\.\d+)?", merchant_p)
            if merchant_re:
                merchant_value = Decimal(merchant_re.group())
            else:
                merchant_value = -Decimal(re.search(r"(?<=贸易商库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", merchant_p).group())

            plastic_woven_re = re.search(r"(?<=原料库存天数较上周上涨)\d+(\.\d+)?", plastic_woven_p)
            if plastic_woven_re:
                plastic_woven_value = Decimal(plastic_woven_re.group())
            else:
                plastic_woven_value = -Decimal(
                    re.search(r"(?<=原料库存天数较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", plastic_woven_p).group())

            bopp_re = re.search(r"(?<=BOPP原料库存较上周上涨)\d+(\.\d+)?", bopp_p)
            if bopp_re:
                bopp_value = Decimal(bopp_re.group())
            else:
                bopp_value = -Decimal(re.search(r"(?<=BOPP原料库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", bopp_p).group())
        else:
            # 2020-07-08之前的DOM结构
            merchant_p = response.css('#content > p:nth-child(30) > span::text').get()
            if merchant_p is not None:
                merchant_re = re.search(r"(?<=贸易商库存较上周增加)\d+(\.\d+)?", merchant_p)
                plastic_woven_p = response.css('#content > p:nth-child(47) > span::text').get().replace(" ", "")
                bopp_p = response.css('#content > p:nth-child(53) > span::text').get()
                if merchant_re:
                    merchant_value = Decimal(merchant_re.group())
                else:
                    merchant_value = -Decimal(
                        re.search(r"(?<=贸易商库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", merchant_p).group())

                plastic_woven_re = re.search(r"(?<=原料库存天数较上周上涨)\d+(\.\d+)?", plastic_woven_p)
                if plastic_woven_re:
                    plastic_woven_value = Decimal(plastic_woven_re.group())
                else:
                    plastic_woven_value = -Decimal(
                        re.search(r"(?<=原料库存天数较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", plastic_woven_p).group())

                bopp_re = re.search(r"(?<=BOPP原料库存较上周上涨)\d+(\.\d+)?", bopp_p)
                if bopp_re:
                    bopp_value = Decimal(bopp_re.group())
                else:
                    bopp_value = -Decimal(re.search(r"(?<=BOPP原料库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", bopp_p).group())
            # 2020-05-13之前的DOM结构
            else:
                merchant_p = response.css('#content > p:nth-child(18) > span::text').get()
                plastic_woven_p = response.css('#content > p:nth-child(35) > span::text').get().replace(" ", "")
                bopp_p = response.css('#content > p:nth-child(41) > span::text').get()

                merchant_re = re.search(r"(?<=贸易商库存较上周增加)\d+(\.\d+)?", merchant_p)
                if merchant_re:
                    merchant_value = Decimal(merchant_re.group())
                else:
                    merchant_value = -Decimal(
                        re.search(r"(?<=贸易商库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", merchant_p).group())

                plastic_woven_re = re.search(r"(?<=原料库存天数较上周上涨)\d+(\.\d+)?", plastic_woven_p)
                if plastic_woven_re:
                    plastic_woven_value = Decimal(plastic_woven_re.group())
                else:
                    plastic_woven_value = -Decimal(
                        re.search(r"(?<=原料库存天数较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", plastic_woven_p).group())

                bopp_re = re.search(r"(?<=BOPP原料库存较上周上涨)\d+(\.\d+)?", bopp_p)
                if bopp_re:
                    bopp_value = Decimal(bopp_re.group())
                else:
                    bopp_value = -Decimal(re.search(r"(?<=BOPP原料库存较上周[\u4e00-\u9fa5]{2})\d+(\.\d+)?", bopp_p).group())

        insert_value(date, merchant_value, self.merchant_index_id)
        insert_value(date, plastic_woven_value, self.plastic_woven_index_id)
        insert_value(date, bopp_value, self.bopp_index_id)
