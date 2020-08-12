# -*- coding: utf-8 -*-
import parsel
import scrapy
import time

from scrapy import FormRequest
from deya_PP.items import DeyaPpItem
from deya_PP.tools import verify_date, get_url
from deya_PP.tools import code_verify


class DeyaPpSSpider(scrapy.Spider):
    name = 'deya_PP_s'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # 识别错误次数
    count = 0

    def start_requests(self):
        pp_url = get_url(self.search_url, '[PP粒]：全国PP装置生产情况汇总')
        pe_url = get_url(self.search_url, '[PE]：国内聚乙烯装置汇总')

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        # 验证pp_url是否是今日的url
        if verify_date(pp_url):
            yield FormRequest(url=self.login_succeed_url, formdata={'username': self.username, 'password': self.password, 'target': pp_url, 'errorPaw': self.errorPaw}, callback=self.parse)

        # 验证pe_url是否是今日的url
        if verify_date(pe_url):
            yield FormRequest(url=self.login_succeed_url, formdata={'username': self.username, 'password': self.password, 'target': pe_url, 'errorPaw': self.errorPaw}, callback=self.parse)

    def parse(self, response):
        title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td/text()").getall()
        temp = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
        content = []
        for t in temp:
            content.append(parsel.Selector(t).xpath("//td/text()").extract())
        item = DeyaPpItem(title=title, content=content)
        yield item
