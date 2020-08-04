# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import time

from deya_cofeed.settings import DRIVER_PATH


class SeleniumMiddleware(object):
    """
    selenium 中间件
    """

    @classmethod
    def process_request(cls, request, spider):
        if spider.name == "deya_cofeed_s":
            options = ChromeOptions()
            options.add_argument('-headless')

            driver = Chrome(executable_path=DRIVER_PATH, chrome_options=options)
            driver.get(request.url)
            time.sleep(0.5)
            uname = driver.find_element_by_xpath('//*[@id="form-login"]/input[1]')
            uname.send_keys("dyzz")
            password = driver.find_element_by_xpath('//*[@id="cofeed_PWD"]')
            password.send_keys("dyzz8576")
            btn = driver.find_element_by_xpath('//*[@id="form-login"]/input[3]')
            btn.click()
            time.sleep(4)
            html = driver.page_source
            driver.quit()

            return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
