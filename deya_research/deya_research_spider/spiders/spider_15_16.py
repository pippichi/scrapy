# 隆众市场价爬虫
# @Author: Jeremy Chan
# @Date: 2020-08-06 10: 03: 55
# @Last Modified by:   Jeremy Chan
#

from scrapy.http import Request, FormRequest
from scrapy.spiders import Spider
from scrapy.selector import Selector

from PIL import Image
from io import BytesIO
from urllib.request import urlretrieve

import datetime
import time
import pytesseract

from deya_research_spider.items import Spider1516Item
from deya_research_spider.tools import code_verify

class Spider1516(Spider):
    name = "Spider1516"
    allowed_domains = ["oilchem.net"]

    url_login = "https://passport.oilchem.net/member/login/login"
    url_code = "https://passport.oilchem.net/member/login/getImgCode"
    url_check_code = "https://passport.oilchem.net/member/login/checkImgCode"
    code_verify_url = 'https://passport.oilchem.net/member/login/checkImgCode?code={code}'
    pp_market_url = "https://dc.oilchem.net/price_search/list.htm?businessType=3&specificationsId=&regionId=&memberId=&standard=&productState=&varietiesId=319&varietiesName=PP粒&templateType=7&flagAndTemplate=3-4%3B2-7%3B1-6%3B6-null&channelId=1777&oneName=塑料&twoName=通用塑料&dateType=0"
    # 休眠时间
    sleep_time = 2
    # 错误集合
    err_list = []
    count = 0

    # host
    host_login_oilchem = 'passport.oilchem.net'
    host_dc_oilchem = 'dc.oilchem.net'

    # 通过xpath获取页面上的内容
    def getXpathContent(self, tr, type):
        index = ''
        content = ''
        if (type == 'indexValue'):
            index = '6'
        elif (type == 'unit'):
            index = '5'
        elif (type == 'remark'):
            index = '2'
        if (tr.xpath("./td[last()-" + index + "]").extract()[0] == '<td></td>'):
            return content
        else:
            xpath_list = [
                "./td[last()-" + index + "]/text()",
            ]
            for xpath_item in xpath_list:
                content = tr.xpath(xpath_item)
                if len(content):
                    break
            return content.extract()[0].strip()

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
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': host,
            # 'Upgrade-Insecure-Requests':'1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        return headers

    def get_headers3(self, host):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': host,
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        return headers

    # 爬虫开始运行
    def start_requests(self):
        return [
            Request(
                url=self.url_code,
                callback=self.getCode,
                dont_filter=True,
                headers=self.get_headers(host=self.host_login_oilchem)
            )
        ]

    # 验证码填写
    def getCode(self, response):
        # # 该方法识别正确率极低
        # open('./code.png', 'wb').write(response.body)
        # # urlretrieve(self.url_code, './code.png')
        # image = Image.open('./code.png')
        # content = pytesseract.image_to_string(image)
        # # 手动输入测试
        # # image = Image.open(BytesIO(response.body))
        # # image.show()
        # # content = input("请输入验证码：")
        # return [
        #     Request(
        #         url=self.url_check_code + "?code=" + content,
        #         callback=self.checkImgCode,
        #         dont_filter=True,
        #         headers=self.get_headers(host=self.host_login_oilchem)
        #     )
        # ]
        temp = code_verify(self.url_code, self.code_verify_url)
        while temp.text != 'true':
            self.count += 1
            print("第{}次识别出错。".format(self.count))
            time.sleep(self.sleep_time)
            temp = code_verify(self.url_code, self.code_verify_url)
        form_data = {
            "username": "rockyeah",
            "password": "cc7da6bca8aa4a5d9c0ebea54fb566ae"
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

    # 验证码校验与登录
    def checkImgCode(self, response):
        if (response.text == 'true'):
            form_data = {
                "username": "rockyeah",
                "password": "cc7da6bca8aa4a5d9c0ebea54fb566ae"
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
        else:
            print("验证码有误，请重新输入！")
            time.sleep(self.sleep_time)
            return [
                Request(
                    url=self.url_code,
                    callback=self.getCode,
                    dont_filter=True,
                    headers=self.get_headers(host=self.host_login_oilchem)
                )
            ]

    # 登录跳转
    def afterLogin(self, response):
        return [
            Request(
                url=self.pp_market_url,
                callback=self.catchMarketValue,
                dont_filter=True,
                headers=self.get_headers3(host=self.host_dc_oilchem)
            )
        ]

    # 开始抓取页面内容
    def catchMarketValue(self, response):
        index_date = datetime.datetime.today().strftime('%Y-%m-%d')
        str_today = datetime.datetime.today().strftime('%m月%d日')
        # index_date = '2020-08-06'
        # str_today = '08月06日'
        sel = Selector(response)
        tables = sel.xpath("//div[@class='tableList shows']")
        # 开始循环读取数据
        for table in tables:
            last_date = table.xpath(".//table/tr")[0].xpath("./th[last()-6]/text()").extract()[0]
            if (str_today == last_date):
                table_trs = table.xpath("./div/table/tr")
                del table_trs[0]
                del table_trs[0]
                area_name = table_trs[0].xpath("./td[last()]/input").attrib["data-region-name"].strip()
                if (area_name == '华东地区' or area_name == '华北地区'):
                    pre_data = {}
                    for tr in table_trs:
                        item = Spider1516Item()
                        unit = self.getXpathContent(tr, "unit")
                        if (unit == '元/吨'):
                            try:
                                td_last = tr.xpath("./td[last()]/input")
                                specificationName = td_last.attrib["data-specifications-name"].strip()
                                regionName = td_last.attrib["data-region-name"].strip()
                                standard = td_last.attrib["data-standard"].strip()
                                price = self.getXpathContent(tr, "indexValue")
                                item['specificationName'] = specificationName
                                item['regionName'] = regionName
                                item['standard'] = standard
                                item['price'] = price
                                item['date'] = index_date
                                pre_data = item

                                yield item
                            except Exception as e:
                                err_content = "{}-{}-{} 对应下一行出现标签无法读取问题({})；".format(
                                    pre_data["regionName"], pre_data["specificationsName"], pre_data["memberAbbreviation"],e)
                                self.err_list.append(err_content)
        print(self.err_list)


