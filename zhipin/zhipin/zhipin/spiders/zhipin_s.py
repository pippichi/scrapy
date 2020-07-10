# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zhipin.items import ZhipinItem


class ZhipinSSpider(CrawlSpider):
    name = 'zhipin_s'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101210100-p100101/?query=Java&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+/?query=Java&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'.+/job_detail/.+\.html'), callback="parse_item",
             follow=False)
    )

    def parse_item(self, response):
        title = response.xpath("//div[@class='info-primary']/div[@class='name']/h1/text()").get()
        salary = response.xpath("//div[@class='info-primary']/div[@class='name']/span/text()").get()
        job_info = response.xpath(
            "//div[contains(@class, 'job-primary')]/div[@class='info-primary']/p//text()").getall()
        if len(job_info) == 3:
            city = job_info[0]
            work_years = job_info[1]
            education = job_info[2]
        elif len(job_info) == 0:
            city, work_years, education = "", "", ""
        elif len(job_info) == 1:
            city = job_info[0]
            work_years, education = "", ""
        else:
            city = job_info[0]
            work_years = job_info[1]
            education = ""
        company_info = response.xpath("//div[contains(@class, 'company-info')]/div[@class='text']//text()").getall()
        compacy_info_res = ""
        for ci in company_info:
            compacy_info_res += ci.strip()
        item = ZhipinItem(title=title, salary=salary, city=city, work_years=work_years, education=education,
                          company_info=compacy_info_res)
        yield item
