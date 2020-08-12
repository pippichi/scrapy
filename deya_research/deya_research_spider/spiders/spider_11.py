import time
from decimal import Decimal

import parsel
import requests
import scrapy
from scrapy import FormRequest

from deya_research_spider.tools import code_verify, insert_value


class Spider11Spider(scrapy.Spider):
    '''
    11.
    供应-pp粉-进口-均聚
    供应-pp粉-进口-共聚
    供应-pp粉-进口-合计
    供应-pp粉-出口-均聚
    供应-pp粉-进口-共聚
    供应-pp粉-进口-合计
    '''
    name = 'spider_11'
    allowed_domains = ['news.oilchem.net']
    start_urls = ['http://news.oilchem.net/']

    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # index_id
    # 供应 - pp粉 - 进口 - 均聚
    import_junju_index_id = 24
    # 供应 - pp粉 - 进口 - 共聚
    import_gongju_index_id = 25
    # 供应 - pp粉 - 进口 - 合计
    import_total_index_id = 26
    # 供应 - pp粉 - 出口 - 均聚
    export_junju_index_id = 27
    # 供应 - pp粉 - 进口 - 共聚
    export_gongju_index_id = 28
    # 供应 - pp粉 - 进口 - 合计
    export_total_index_id = 29

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': 'PP粒进出口数据简析'}).text)
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
        # 进口数据
        import_1 = response.xpath("//div[@id='content']//tr[2]/td[2]/text()").extract_first()
        import_2 = response.xpath("//div[@id='content']//tr[2]/td[3]/text()").extract_first()
        import_3 = response.xpath("//div[@id='content']//tr[2]/td[4]/text()").extract_first()
        import_junju = Decimal(import_1)
        import_gongju = Decimal(import_2) + Decimal(import_3)
        import_total = Decimal(import_1) + Decimal(import_2) + Decimal(import_3)

        # 出口数据
        export_1 = response.xpath("//div[@id='content']//tr[2]/td[6]/text()").extract_first()
        export_2 = response.xpath("//div[@id='content']//tr[2]/td[7]/text()").extract_first()
        export_3 = response.xpath("//div[@id='content']//tr[2]/td[8]/text()").extract_first()
        export_junju = Decimal(export_1)
        export_gongju = Decimal(export_2) + Decimal(export_3)
        export_total = Decimal(export_1) + Decimal(export_2) + Decimal(export_3)

        # 插入
        insert_value(date, import_junju, self.import_junju_index_id)
        insert_value(date, import_gongju, self.import_gongju_index_id)
        insert_value(date, import_total, self.import_total_index_id)
        insert_value(date, export_junju, self.export_junju_index_id)
        insert_value(date, export_gongju, self.export_gongju_index_id)
        insert_value(date, export_total, self.export_total_index_id)



class Spider11SpiderHistory(scrapy.Spider):
    '''
    11.历史爬虫
    供应-pp粉-进口-均聚
    供应-pp粉-进口-共聚
    供应-pp粉-进口-合计
    供应-pp粉-出口-均聚
    供应-pp粉-进口-共聚
    供应-pp粉-进口-合计
    '''
    name = 'spider_11_history'
    allowed_domains = ['news.oilchem.net']
    start_urls = ['http://news.oilchem.net/']

    search_url = "https://search.oilchem.net/solrSearch/select.htm"
    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'

    # index_id
    # 供应 - pp粉 - 进口 - 均聚
    import_junju_index_id = 24
    # 供应 - pp粉 - 进口 - 共聚
    import_gongju_index_id = 25
    # 供应 - pp粉 - 进口 - 合计
    import_total_index_id = 26
    # 供应 - pp粉 - 出口 - 均聚
    export_junju_index_id = 27
    # 供应 - pp粉 - 进口 - 共聚
    export_gongju_index_id = 28
    # 供应 - pp粉 - 进口 - 合计
    export_total_index_id = 29

    # 识别错误次数
    count = 0

    def start_requests(self):
        response = parsel.Selector(
            requests.post(self.search_url, {'pageNo': '1', 'keyword': 'PP粒进出口数据简析'}).text)
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
        # 进口数据
        import_1 = response.xpath("//div[@id='content']//tr[2]/td[2]/text()").extract_first()
        import_2 = response.xpath("//div[@id='content']//tr[2]/td[3]/text()").extract_first()
        import_3 = response.xpath("//div[@id='content']//tr[2]/td[4]/text()").extract_first()
        import_junju = Decimal(import_1)
        import_gongju = Decimal(import_2) + Decimal(import_3)
        import_total = Decimal(import_1) + Decimal(import_2) + Decimal(import_3)

        # 出口数据
        export_1 = response.xpath("//div[@id='content']//tr[2]/td[6]/text()").extract_first()
        export_2 = response.xpath("//div[@id='content']//tr[2]/td[7]/text()").extract_first()
        export_3 = response.xpath("//div[@id='content']//tr[2]/td[8]/text()").extract_first()
        export_junju = Decimal(export_1)
        export_gongju = Decimal(export_2) + Decimal(export_3)
        export_total = Decimal(export_1) + Decimal(export_2) + Decimal(export_3)

        # 插入
        insert_value(date, import_junju, self.import_junju_index_id)
        insert_value(date, import_gongju, self.import_gongju_index_id)
        insert_value(date, import_total, self.import_total_index_id)
        insert_value(date, export_junju, self.export_junju_index_id)
        insert_value(date, export_gongju, self.export_gongju_index_id)
        insert_value(date, export_total, self.export_total_index_id)

