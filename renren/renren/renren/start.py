"""
 -*- coding: utf-8 -*-
@File    : start.py
@Time    : 6/12/20 1:33 PM
@Author   : qyf
Connect  : emoqyf@sina.com
@Software: Linux python3.6.8 Django2.0
"""

from scrapy import cmdline

cmdline.execute("scrapy crawl renren_spider".split())
