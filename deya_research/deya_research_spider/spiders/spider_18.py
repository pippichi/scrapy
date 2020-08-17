import datetime
import json
import random
import time
import scrapy
from scrapy import Request, FormRequest
from deya_research_spider.tools import insert_value, code_verify


class Spider18Spider(scrapy.Spider):
    """
    18.丙烯制品
    """
    # host
    host_login_oilchem = 'passport.oilchem.net'
    host_dc_oilchem = 'dc.oilchem.net'

    # header封装
    def get_headers(self, host):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': host,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        return headers

    def get_headers2(self, host):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": host,
            "Origin": "https://dc.oilchem.net",
            "Referer": "https://dc.oilchem.net/price_search/detail.htm?channelId=1993&varietiesId=479&id=5460&timeType=0&flag=1&businessType=3",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        return headers

    name = 'spider_18'
    allowed_domains = ['oilchem.net']

    username = 'rockyeah'
    password = 'cc7da6bca8aa4a5d9c0ebea54fb566ae'
    errorPaw = 'deya1589'
    url_login = "https://passport.oilchem.net/member/login/login"
    url_code = "https://passport.oilchem.net/member/login/getImgCode"
    url_check_code = "https://passport.oilchem.net/member/login/checkImgCode"
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'

    # 指标在数据库中的id
    bingxijing_id = 8
    huanyangbingwan_id = 9
    xinchun_id = 10
    bingxisuan_id = 11

    # id对应名称
    id_name = {bingxijing_id: "丙烯腈",
               huanyangbingwan_id: "环氧丙烷",
               xinchun_id: "辛醇",
               bingxisuan_id: "丙烯酸"}

    # 爬虫开始时间
    queryStartTime = "20200711"

    search_urls = [({
                        'channelId': '1993',
                        'varietiesId': '479',
                        'businessId': '5460',
                        'businessType': '3',
                        'queryStartTime': queryStartTime,
                        'queryEndTime': datetime.date.today().strftime("%Y%m%d"),
                        'indexType': '0',
                        'pageSize': '20'
                    }, bingxijing_id),
                   ({
                        "channelId": "1876",
                        "varietiesId": "157",
                        "businessId": "5032",
                        "businessType": "3",
                        "queryStartTime": queryStartTime,
                        "queryEndTime": datetime.date.today().strftime("%Y%m%d"),
                        "indexType": "0",
                        "pageSize": "20"
                    }, huanyangbingwan_id),
                   ({
                        "channelId": "2079",
                        "varietiesId": "3144",
                        "businessId": "6022",
                        "businessType": "3",
                        "queryStartTime": queryStartTime,
                        "queryEndTime": datetime.date.today().strftime("%Y%m%d"),
                        "indexType": "0",
                        "pageSize": "20",
                    }, xinchun_id),
                   ({
                        "channelId": "1844",
                        "varietiesId": "163",
                        "businessId": "6855",
                        "businessType": "3",
                        "queryStartTime": queryStartTime,
                        "queryEndTime": datetime.date.today().strftime("%Y%m%d"),
                        "indexType": "0",
                        "pageSize": "20",
                    }, bingxisuan_id)]

    login_succeed_url = 'https://passport.oilchem.net/member/login/login'
    timestamp = int(round(time.time() * 1000))
    img_url = 'https://passport.oilchem.net/member/login/getImgCode?timestamp=' + str(timestamp)

    # mode为0是爬每日最新， mode为1是爬历史数据
    mode = 0

    def start_requests(self):
        yield Request(
            url=self.url_code,
            callback=self.getCode,
            dont_filter=True,
            headers=self.get_headers(host=self.host_login_oilchem)
        )

    # 验证码填写
    def getCode(self, response):
        temp = code_verify(self.url_code, self.code_verify_url)
        count = 0
        while temp.text != 'true':
            count += 1
            print("第{}次识别出错。".format(count))
            time.sleep(0.5)
            temp = code_verify(self.url_code, self.code_verify_url)
        form_data = {
            "username": "rockyeah",
            "password": "cc7da6bca8aa4a5d9c0ebea54fb566ae",
            'errorPaw': "deya1589",
        }
        return [
            FormRequest(
                url=self.url_login,
                callback=self.afterLogin,
                formdata=form_data,
                dont_filter=True,
                headers=self.get_headers(self.host_login_oilchem)
            )
        ]

    # 登录跳转
    def afterLogin(self, response):
        for su in self.search_urls:
            formdata = su[0]
            obj_id = su[1]
            formdata['pageNumber'] = "1"
            yield FormRequest(
                    url='https://dc.oilchem.net/price_search/history.htm',
                    formdata=formdata,
                    callback=self.parse,
                    dont_filter=True,
                    headers=self.get_headers2(host=self.host_dc_oilchem),
                    meta={'obj_id': obj_id, 'formdata': formdata}
                  )

    def parse(self, response, **kwargs):
        try:
            content = json.loads(response.text)
            obj_id = response.meta['obj_id']
            if self.mode == 1:
                formdata = response.meta['formdata']
                pages = content['pages']
                for c in content['pageInfo']['list']:
                    date = c['indexDate'].replace("/", "-")
                    value = c['indexValue']
                    insert_value(date, value, obj_id)
                for p in range(2, int(pages)+1):
                    formdata['pageNumber'] = str(p)
                    yield FormRequest(
                        url='https://dc.oilchem.net/price_search/history.htm',
                        formdata=formdata,
                        callback=self.parse_next_page,
                        dont_filter=True,
                        headers=self.get_headers2(host=self.host_dc_oilchem),
                        meta={'obj_id': obj_id, 'formdata': formdata}
                    )
                    time.sleep(1 + int(random.uniform(5, 10)))
            else:
                date = content['pageInfo']['list'][0]['indexDate'].replace("/", "-")
                if date != datetime.date.today().strftime("%Y-%m-%d"):
                    print("今日" + self.id_name[obj_id] + "还没出来")
                else:
                    value = content['pageInfo']['list'][0]['indexValue']
                    insert_value(date, value, obj_id)
        except Exception as e:
            print('!' * 30)
            print(e)
            print('!' * 30)

    def parse_next_page(self, response):
        try:
            content = json.loads(response.text)
            obj_id = response.meta['obj_id']
            if self.mode == 1:
                for c in content['pageInfo']['list']:
                    date = c['indexDate'].replace("/", "-")
                    value = c['indexValue']
                    insert_value(date, value, obj_id)
            else:
                pass
        except Exception as e:
            print('!' * 30)
            print(e)
            print('!' * 30)
