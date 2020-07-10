# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests

from jianshu.models import ProxyModel


class UserAgentDownloadMiddleware:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.    0.3538.77 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.    2919.83 Safari/537.36'
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers["User-Agent"] = user_agent


class IPProxyDownloadMiddleware:
    def __init__(self, ip_pool):
        self.ip_pool = ip_pool

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ip_pool=crawler.settings.get('IP_POOL')
        )

    def _get_random_ip(self):
        try:
            response = requests.get(self.ip_pool)
        except Exception:
            return None
        if response.status_code == 200:
            return response.text.strip()

    def process_request(self, request, spider):
        pm = ProxyModel(self._get_random_ip())
        request.meta['proxy'] = pm.get_ip
