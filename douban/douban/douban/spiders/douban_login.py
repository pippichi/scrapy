# -*- coding: utf-8 -*-
import scrapy
from urllib import request
import requests
from PIL import Image
from base64 import b64encode


class DoubanLoginSpider(scrapy.Spider):
    name = 'douban_login'
    allowed_domains = ['douban.com']
    start_urls = ['http://accounts.douban.com/login']
    login_url = 'http://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/9795064/'
    editsignature_url = 'https://www.douban.com/j/people/97956064/edit_signature'

    def parse(self, response):
        formdata = {
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '874496049@qq.com',
            'form_password': 'qyfnig107',
            'remember': 'on',
            'login': '登录'
        }

        captcha_url = response.xpath('//img[@id="captcha_image"]/@src').get()
        if captcha_url:
            captcha = self.recognize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').get()
            formdata['captcha-id'] = captcha_id
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_after_login)

    # def recognize_captcha(self, url):
    #     request.urlretrieve(url, 'captcha.png')
    #     image = Image.open('captcha.png')
    #     image.show()
    #     captcha = input("输入验证码: ")
    #     return captcha

    def recognize_captcha(self, image_url):
        captcha_url = image_url
        request.urlretrieve(captcha_url, 'captcha.png')
        recognize_url = 'http://jisuyzmsb.market.alicloudapi.com/captcha/recognize?type=e'
        formdata = {}
        with open('captcha.png', 'rb') as f:
            data = f.read()
            pic = b64encode(data)
            formdata['pic'] = pic

        appcode = '买了自动识别网站就会给你这个code'
        headers = {
            'Content-Type': 'application/x-www-form-urlencode;charset-UTF-8',
            'Authorization': 'APPCODE ' + appcode
        }

        response = requests.post(recognize_url, data=formdata, headers=headers)
        result = response.json()
        code = result['result']['code']
        return code

    def parse_after_login(self, response):
        if response.url == 'https://www.douban.com/':
            yield scrapy.Request(self.profile_url, callback=self.parse_profile)
            print('login succ')
        else:
            print('login err')
    def parse_profile(self, response):
        if response.url == self.profile_url:
            ck = response.xpath("//input[@name='ck']/@value").get()
            formdata = {
                'ck': ck,
                'signature': 'i am a robot, do not make me angry, or i will kill you all!'
            }
            yield scrapy.FormRequest(self.editsignature_url, formdata=formdata, callback=self.parse_none)
        else:
            print('profile edit failed')

    # 没有给formdata指定callback的话scrapy就会自动执行parse函数，而且执行的url就是当前formdata的url，为了避免这种情况，我们给他指定一个空的方法
    def parse_none(self):
        pass
