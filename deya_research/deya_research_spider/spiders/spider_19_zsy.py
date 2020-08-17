import re
import time

import parsel
import requests
import scrapy
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider19ZsySpiderHB(scrapy.Spider):
    '''
    PP出厂价：中石油：华北 （每日爬取）
    '''
    name = 'spider_19_zsy_hb'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 61

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华北PP'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']//text()").get()
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
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row+1}]")
        prices = []
        count = 1
        for tr in tr_list:
            if count == 1:
                price = tr.xpath('./td[5]//text()').extract_first()
            else:
                price = tr.xpath('./td[4]//text()').extract_first()
            count += 1
            prices.append(int(price))
        price = min(prices)
        insert_value(date, price, self.index_id)


class Spider19ZsySpiderHD(scrapy.Spider):
    '''
    PP出厂价：中石油：华东 （每日爬取）
    '''
    name = 'spider_19_zsy_hd'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 62

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华东PP'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']//text()").get()
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
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row+1}]")
        prices = []
        count = 1
        for tr in tr_list:
            if count == 1:
                price = tr.xpath('./td[4]//text()').extract_first()
            else:
                price = tr.xpath('./td[3]//text()').extract_first()
            count += 1
            prices.append(int(price))
        price = min(prices)
        insert_value(date, price, self.index_id)

class Spider19ZsySpiderHN(scrapy.Spider):
    '''
    PP出厂价：中石油：华南 （每日爬取）
    '''
    name = 'spider_19_zsy_hn'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 63

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华南PP'}).text)
        url = response.xpath("//ul[@class='contentList']/li[1]//a/@href").get()
        date = response.xpath("//ul[@class='contentList']/li[1]//span[@class='date']//text()").get()
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
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row+1}]")
        prices = []
        count = 1
        for tr in tr_list:
            if count == 1:
                price = tr.xpath('./td[4]//text()').extract_first()
            else:
                price = tr.xpath('./td[3]//text()').extract_first()
            count += 1
            prices.append(int(price))
        price = min(prices)
        insert_value(date, price, self.index_id)




class Spider19ZsySpiderHBHistory(scrapy.Spider):
    '''
    PP出厂价：中石油：华北 （历史爬取）
    '''
    name = 'spider_19_zsy_hb_history'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 61

    # 识别错误次数
    count = 0

    def start_requests(self):

        # 获取最大页数
        res = requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华北PP'}).text
        maxPageNo = re.findall(r"第1页/共 (\d+)页", res)[0]

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        # 每页爬取
        for pageNo in range(1,int(maxPageNo)+1):
            response = parsel.Selector(
                requests.post(self.search_url, {'pageNo': str(pageNo), 'keyword': '[PP粒]：中油华北PP'}).text)
            items = response.xpath("//ul[@class='contentList']/li").getall()



            for item in items:
                time.sleep(1)
                url = parsel.Selector(item).xpath("//h2//a/@href").get()
                date = parsel.Selector(item).xpath("//span[@class='date']//text()").get()
                data = {
                    'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
                }
                if date:
                    yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})




    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row+1}]")
        prices = []
        count = 1
        for tr in tr_list:
            if count == 1:
                price = tr.xpath('./td[5]//text()').extract_first()
            else:
                price = tr.xpath('./td[4]//text()').extract_first()
            # 26页之后特殊情况：将数字拆分到不同的标签
            if int(price) < 1000:
                if count == 1:
                    price = tr.xpath('./td[5]//text()').extract()
                else:
                    price = tr.xpath('./td[4]//text()').extract()
                price = ''.join(price)

            # 2019-9-9开始数据的列发生变化
            if date <= "2019-09-09":
                if count == 1:
                    price = tr.xpath('./td[4]//text()').extract_first()
                else:
                    price = tr.xpath('./td[3]//text()').extract_first()
                # 26页之后特殊情况：将数字拆分到不同的标签
                if int(price) < 1000:
                    if count == 1:
                        price = tr.xpath('./td[4]//text()').extract()
                    else:
                        price = tr.xpath('./td[3]//text()').extract()
                    price = ''.join(price)

            count += 1
            try:
                # 有缺失值为"-"，报异常，跳过
                prices.append(int(price))
            except Exception as e:
                pass
        price = min(prices)
        insert_value(date, price, self.index_id)


class Spider19ZsySpiderHDHistory(scrapy.Spider):
    '''
    PP出厂价：中石油：华东 （历史爬取）
    '''
    name = 'spider_19_zsy_hd_history'
    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 62

    # 识别错误次数
    count = 0

    def start_requests(self):

        # 获取最大页数
        res = requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华东PP'}).text
        maxPageNo = re.findall(r"第1页/共 (\d+)页", res)[0]

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        # 每页爬取
        for pageNo in range(30,int(maxPageNo)+1):
            response = parsel.Selector(
                requests.post(self.search_url, {'pageNo': str(pageNo), 'keyword': '[PP粒]：中油华东PP'}).text)
            items = response.xpath("//ul[@class='contentList']/li").getall()

            for item in items:
                time.sleep(2)
                url = parsel.Selector(item).xpath("//h2//a/@href").get()
                date = parsel.Selector(item).xpath("//span[@class='date']//text()").get()
                data = {
                    'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
                }
                if date:
                    yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row + 1}]")
        prices = []
        price = None
        for tr in tr_list:
            # 拿到每行的文本，再正则匹配（较好）
            text_list = tr.xpath('.//text()').extract()
            for i in text_list:
                if re.findall(r"^(\d\d\d\d)$", i):
                    price = re.findall(r"^(\d\d\d\d)$", i)[0]

            try:
                # 有缺失值为"-"，报异常，跳过
                prices.append(int(price))
            except Exception as e:
                pass
        price = min(prices)
        # print('*' * 50)
        # print(date)
        # print(prices)
        # print('*' * 50)
        insert_value(date, price, self.index_id)



class Spider19ZsySpiderHNHistory(scrapy.Spider):
    '''
    PP出厂价：中石油：华南 （历史爬取）
    '''
    name = 'spider_19_zsy_hn_history'

    allowed_domains = ['news.oilchem.net']
    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    index_id = 63

    # 识别错误次数
    count = 0

    def start_requests(self):

        # 获取最大页数
        res = requests.post(self.search_url, {'pageNo': '1', 'keyword': '[PP粒]：中油华南PP'}).text
        maxPageNo = re.findall(r"第1页/共 (\d+)页", res)[0]

        temp = code_verify(self.img_url, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            temp = code_verify(self.img_url, self.code_verify_url)

        # 每页爬取
        for pageNo in range(1,int(maxPageNo)+1):
            response = parsel.Selector(
                requests.post(self.search_url, {'pageNo': str(pageNo), 'keyword': '[PP粒]：中油华南PP'}).text)
            items = response.xpath("//ul[@class='contentList']/li").getall()



            for item in items:
                time.sleep(2)
                url = parsel.Selector(item).xpath("//h2//a/@href").get()
                date = parsel.Selector(item).xpath("//span[@class='date']//text()").get()
                data = {
                    'username': self.username, 'password': self.password, 'target': url, 'errorPaw': self.errorPaw
                }
                if date:
                    yield FormRequest(url=self.login_succeed_url, formdata=data, callback=self.parse, meta={'date': date})

    def parse(self, response, **kwargs):
        date = response.meta.get('date')
        row = response.xpath("//div[@id='content']//tbody/tr[2]/td[1]/@rowspan").get()
        row = int(row)
        tr_list = response.xpath(f"//div[@id='content']//tbody/tr[position()>1][position()<{row + 1}]")
        prices = []
        price = None
        for tr in tr_list:
            text_list = tr.xpath('.//text()').extract()
            for i in text_list:
                if re.findall(r"^(\d\d\d\d)$", i):
                    price = re.findall(r"^(\d\d\d\d)$", i)[0]

            try:
                # 有缺失值为"-"，报异常，跳过
                prices.append(int(price))
            except Exception as e:
                pass
        price = min(prices)
        # print('*' * 50)
        # print(date)
        # print(prices)
        # print('*' * 50)
        insert_value(date, price, self.index_id)