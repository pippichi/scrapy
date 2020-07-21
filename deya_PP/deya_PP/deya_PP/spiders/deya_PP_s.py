# -*- coding: utf-8 -*-
import scrapy
import requests

from urllib.request import urlretrieve
from PIL import Image

import time
import parsel
import pytesseract

from scrapy import FormRequest
from deya_PP.items import DeyaPpItem
from deya_PP.tools import verify_date, failed_and_send_email


def title_and_content(response):
    title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td/text()").getall()
    temp = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
    content = []
    for t in temp:
        content.append(parsel.Selector(t).xpath("//td/text()").extract())
    return title, content


class DeyaPpSSpider(scrapy.Spider):
    name = 'deya_PP_s'
    allowed_domains = ['news.oilchem.net']
    start_urls = None
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：全国PP装置生产情况汇总'}).text)
        self.start_urls = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()

        # 验证url是否是今日的url
        flag = verify_date(self.start_urls)
        if not flag:
            failed_and_send_email()
            return

        urlretrieve(self.img_url, './PP_code.png')
        image = Image.open('./PP_code.png')
        content = pytesseract.image_to_string(image)
        requests.get(self.code_verify_url.format(code=content))
        yield FormRequest(url=self.login_succeed_url, formdata={'username': self.username, 'password': self.password, 'target': self.start_urls, 'errorPaw': self.errorPaw}, callback=self.parse)

    def parse(self, response):
        title = response.xpath("//div[@id='content']//tr[@class='firstRow']/td/text()").getall()
        temp = response.xpath("//div[@id='content']//tr[not(contains(@class, 'firstRow'))]").getall()
        content = []
        for t in temp:
            content.append(parsel.Selector(t).xpath("//td/text()").extract())
        item = DeyaPpItem(title=title, content=content)
        yield item
