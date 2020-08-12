# 大商所PP合约日成交持仓情况
# @Author: Jeremy Chan
# @Date: 2020-08-07 14: 03: 55
# @Last Modified by:   Jeremy Chan
#
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from deya_research_spider.items import Spider17Item

import time
import datetime
import re
import pandas as pd
import requests as req

class Spider17(Spider):
    name = "Spider17"

    # 聚丙烯日成交持仓（大连商品交易所）
    memberDealPosiQuotesUrl = "http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html"

    # 仓单日报
    wbillWeeklyQuotesUrl = "http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html"

    # 今日日期
    str_today_date = datetime.date.today().strftime('%Y-%m-%d')
    today_date = datetime.date.today()
    # today_date = datetime.date(2020, 8, 7)
    # str_today_date = datetime.date(2020, 8, 7).strftime('%Y-%m-%d')
    # today_date = today_date - datetime.timedelta(days=1)
    year = today_date.year
    month = today_date.month
    date = today_date.day

    # 休眠时间
    sleep_time = 2

    # host
    host_dce = 'www.dce.com.cn'

    # 当前合约
    current_contract = ''

    # header封装
    def get_headers(self, host):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': host,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        return headers

        # 通过xpath获取页面上的内容
    def getXpathContent(self, tr, index):
        # index = ''
        content = ''
        # if (type == 'zyhdlldpe_product_ID'):
        #     index = '6'
        # elif (type == 'unitValuationName'):
        #     index = '5'
        # elif (type == 'remark'):
        #     index = '2'
        if (index != "0"):
            xpath_list = [
                "td[" + index + "]/text()",
                "td[" + index + "]/a/text()",
                "td[" + index + "]/span/text()",
                "td[" + index + "]/span/span/text()",
                "td[" + index + "]/span/span/span/text()"
            ]
        else:
            xpath_list = [
                "text()",
            ]
        for xpath_item in xpath_list:
            content = tr.xpath(xpath_item)
            if len(content):
                break
        return content.extract()[0].strip()

    # 爬虫开始
    def start_requests(self):
        # form_data = {
        #     "wbillWeeklyQuotes.variety": "pp",
        #     "year": str(self.year),
        #     "month": str(self.month - 1),
        #     "day": str(self.date),
        # }
        # return [
        #     FormRequest(
        #         # headers = self.get_headers(self.host_dce),
        #         url = self.wbillWeeklyQuotesUrl,
        #         formdata = form_data,
        #         meta={'date': self.str_today_date},
        #         dont_filter = True,
        #         callback = self.w_bill_weekly_quotes
        #     )
        # ]

        # # 历史仓单日数据 （目前暂时使用excel下载来的数据直接导入，详情见 data_excel/spider_17/pp_cd.py）
        # date_list = pd.date_range(start='2017-01-01', end='2017-01-31')
        # for date in date_list:
        #     form_data = {
        #         "wbillWeeklyQuotes.variety": "pp",
        #         "year": str(date.year),
        #         "month": str(date.month - 1),
        #         "day": str(date.day),
        #     }
        #     yield FormRequest(
        #         # headers = self.get_headers(self.host_dce),
        #         url = self.wbillWeeklyQuotesUrl,
        #         formdata = form_data,
        #         meta= {'date': date.strftime('%Y-%m-%d')},
        #         dont_filter = True,
        #         callback = self.w_bill_weekly_quotes
        #     )

        # 历史日成交持仓
        date_list = pd.date_range(start='2017-08-01', end='2017-08-02')
        contract_url = 'http://service.99qh.com/hold2/MemberHold/GetAgreementInfo.aspx?date={}&goodsid=84'
        for date in date_list:
            str_date = date.strftime('%Y-%m-%d')
            new_contract_url = contract_url.format(str_date)
            # time.sleep(self.sleep_time)
            yield Request(
                dont_filter = True,
                url = new_contract_url,
                meta = {'date': str_date},
                callback = self.get_contract_hst
            )


    # 仓单日报
    def w_bill_weekly_quotes(self, response):
        if (response.status == 200):
            item = Spider17Item()
            title_num = {}
            sel = Selector(response)
            c_date = response.meta['date']
            contents = sel.xpath("//div[@class='dataArea']/table/tr")
            if (len(contents) > 2):
                titles = sel.xpath("//div[@class='dataArea']/table/tr/th")
                for title in titles:
                    title_name = ''.join(title.xpath("text()").extract())
                    result = re.findall(r'品种|今日仓单量', title_name)
                    if (len(result)):
                        result_name = result[0]
                        title_num[result_name] = titles.index(title) + 1
                del contents[0]
                for content in contents:
                    product_name = self.getXpathContent(content, str(title_num['品种']))
                    if product_name == '聚丙烯小计':
                        value = self.getXpathContent(content, str(title_num['今日仓单量']))
                        item['value'] = value
                        item['type'] = '仓单量'
                        item['date'] = c_date
                        item['rank'] = '1'
                        item['memberName'] = '仓单'
                        item['contract'] = '无'
                        break
                yield item
            time.sleep(self.sleep_time)

        form_data = {
            "memberDealPosiQuotes.variety": "pp",
            "memberDealPosiQuotes.trade_type": "0",
            "year": str(self.year),
            "month": str(self.month - 1),
            "day": str(self.date),
            "contract.contract_id": "",
            "contract.variety_id": "pp",
            "contract": ""
        }
        time.sleep(self.sleep_time)
        yield FormRequest(
            # headers = self.get_headers(self.host_dce),
            url=self.memberDealPosiQuotesUrl,
            formdata=form_data,
            dont_filter=True,
            callback=self.get_contract
        )

    # 获取当前主力合约
    def get_contract(self, response):
        if (response.status == 200):
            form_data = {
                "memberDealPosiQuotes.variety": "pp",
                "memberDealPosiQuotes.trade_type": "0",
                "year": str(self.year),
                "month": str(self.month - 1),
                "day": str(self.date),
                "contract.contract_id": '',
                "contract.variety_id": "pp",
                "contract": ""
            }
            contract_list = []
            sel = Selector(response)
            contract_contents = sel.xpath('//li[@class="keyWord_65"]/text()').extract()
            for contract_content in contract_contents:
                result = contract_content.strip()
                if (len(result)):
                    contract_list.append(result)
            for contract in contract_list:
                contract_result = re.findall(r'01|05|09', contract)
                if (len(contract_result)):
                    current_contract = contract_result[0]
                    form_data['contract.contract_id'] = contract
                    yield FormRequest(
                        # headers = self.get_headers(self.host_dce),
                        url=self.memberDealPosiQuotesUrl,
                        formdata=form_data,
                        meta={'current_contract': current_contract},
                        dont_filter=True,
                        callback=self.deal_daily_dce
                    )

    # 日成交持仓
    def deal_daily_dce(self, response):
        if (response.status == 200):
            sel = Selector(response)
            current_contract = response.meta['current_contract']
            contract = current_contract
            title_nums = {}
            # 总计部分
            total_contents = sel.xpath("//div[@class='dataArea']/table[1]/tr[2]")
            total_titles = sel.xpath("//div[@class='dataArea']/table[1]/tr[1]/th")
            for title in total_titles:
                title_name = ''.join(title.xpath("text()").extract())
                result = re.findall(r'总持买单量|总持卖单量', title_name)
                if (len(result)):
                    result_name = result[0]
                    title_nums[result_name] = total_titles.index(title) + 1
            for title_num in title_nums:
                item = Spider17Item()
                value = self.getXpathContent(total_contents, str(title_nums[title_num]))
                item['type'] = title_num
                item['value'] = value
                item['date'] = self.str_today_date
                item['rank'] = '1'
                item['memberName'] = '期货公司会员'
                item['contract'] = contract
                yield item

            # 各项排名部分(名次-会员简称-持买单量/持卖单量)
            part_title_nums = {}
            part_contents = sel.xpath("//div[@class='dataArea']/table[2]/tr")
            part_titles = sel.xpath("//div[@class='dataArea']/table[2]/tr/th")
            for title in part_titles:
                title_name = self.getXpathContent(title, "0")
                result = re.findall(r'持买单量|持卖单量', title_name)
                if (len(result)):
                    result_name = result[0]
                    part_title_nums[result_name] = part_titles.index(title) + 1
            del part_contents[0]
            del part_contents[-1]
            for part_content in part_contents:
                for part_title in part_title_nums:
                    item = Spider17Item()
                    index = part_title_nums[part_title]
                    item['rank'] = self.getXpathContent(part_content, str(index - 2))
                    item['memberName'] = self.getXpathContent(part_content, str(index - 1))
                    item['value'] = self.getXpathContent(part_content, str(index))
                    item['date'] = self.str_today_date
                    item['type'] = part_title
                    item['contract'] = contract
                    yield item

    # 获取当前主力合约 —— 历史（99期货）
    def get_contract_hst(self, response):
        sel = Selector(response)
        current_date = response.meta['date']
        table_url = 'http://service.99qh.com/hold2/MemberHold/GetTableHtml.aspx?date={}&user=99qh&goods=84&agreement={}&count=20'
        agreement_contents = sel.xpath('//AgreementCode/text()').extract()
        if (len(agreement_contents)):
            for agreement_code in agreement_contents:
                contract_result = re.findall(r'01|05|09', agreement_code)
                if (len(contract_result)):
                    new_table_url = table_url.format(current_date, agreement_code)
                    yield Request(
                        dont_filter=True,
                        url=new_table_url,
                        meta={'current_date': current_date, 'current_contract': contract_result[0]},
                        callback=self.deal_daily_dce_hst
                    )

    # 日成交持仓 —— 历史（99期货）
    def deal_daily_dce_hst(self,response):
        if (response.status == 200):
            sel = Selector(response)
            current_date = response.meta['current_date']
            current_contract = response.meta['current_contract']
            title_nums = {}
            title_to_type = {
                '多仓': '持买单量',
                '空仓': '持卖单量'
            }
            contents = sel.xpath('//table[1]/tr')
            titles = sel.xpath('//table[1]/tr[2]/td')
            for title in titles:
                title_name = self.getXpathContent(title, "0")
                result = re.findall(r'多仓|空仓', title_name)
                if (len(result)):
                    result_name = result[0]
                    title_nums[title_to_type[result_name]] = titles.index(title) + 1
            del contents[0]
            del contents[0]
            del contents[0]
            for content in contents:
                for title in title_nums:
                    item = Spider17Item()
                    index = title_nums[title]
                    rank = self.getXpathContent(content, str(index - 2))
                    value = self.getXpathContent(content, str(index))
                    if (len(value) > 0):
                        if (len(re.findall('合计|总计', rank))):
                            item['rank'] = '1'
                            item['memberName'] = '期货公司会员'
                            item['type'] = '总' + title
                        else:
                            item['rank'] = rank
                            item['type'] = title
                            item['memberName'] = self.getXpathContent(content, str(index - 1))
                        item['value'] = value
                        item['date'] = current_date
                        item['contract'] = current_contract
                        yield item


