# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Request
import parsel

from jydb.items import JydbItem


class JydbSpiderSpider(scrapy.Spider):
    name = 'jydb_spider'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=胶原蛋白&ie=utf-8&pn=0']

    base = "https://"
    detail_base = "https://tieba.baidu.com"

    def parse(self, response):
        # 获取下一页url
        url_pattern = re.compile(
            '<div class="thread_list_bottom clearfix">.*?>(.*?)</div>',
            re.S
        )
        url = re.findall(url_pattern, response.text)[0]
        data = parsel.Selector(url)

        url = data.xpath('//a[last()-1]/@href').extract()[0].strip('//')

        # 获取detail的url
        detail_url_pattern = re.compile(
            '<div class="content".*?<div id="content_leftList".*?<ul.*?>(.*?)</ul>',
            re.S
        )
        detail_li = re.findall(detail_url_pattern, response.text)[0].strip()

        detail_data = parsel.Selector(detail_li)
        detail_url = detail_data.xpath('//div[contains(@class, "col2_right")]/div/div/a/@href').extract()
        for d_url in detail_url:
            yield Request(self.detail_base + d_url, callback=self.parse_detail)

        yield Request(self.base + url, callback=self.parse)

    def parse_detail(self, response):
        # title
        title_pattern = re.compile(
            '<div class="core_title core_title_theme_bright".*?<h1.*?>(.*?)</h1>',
        re.S)
        title = re.findall(title_pattern, response.text)[0]

        # content
        content_pattern = re.compile(
            '<div class="left_section".*?<div class="p_postlist".*?>(.*?)<div class="pb_footer">',
        re.S)
        contents = re.findall(content_pattern, response.text)[0]
        content_temp = parsel.Selector(contents)
        content = content_temp.xpath('//div[@class="d_post_content_main"]/div/cc/div[contains(@class, "d_post_content")]//text()').extract()

        # # comments
        # comments = content_temp.xpath('//div[@class="d_post_content_main"]/div[2]/div[2]')

        item = JydbItem(title=title, content=content)
        yield item

        temp_pattern = re.compile(
            '<div class="pb_footer">.*?<li.*?>(.*?)</li>',
            re.S
        )
        next_url_a = re.findall(temp_pattern, response.text)[0].strip()
        next_url_a_parsel = parsel.Selector(next_url_a)
        next_url = next_url_a_parsel.xpath('//a[last()-1]/@href').extract()
        if len(next_url) != 0:
            yield Request(self.detail_base + next_url[0], callback=self.parse_detail)
