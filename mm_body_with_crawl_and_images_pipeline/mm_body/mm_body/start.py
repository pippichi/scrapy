"""
 -*- coding: utf-8 -*-
@File    : start.py
@Time    : 6/19/20 12:55 AM
@Author   : qyf
Connect  : emoqyf@sina.com
@Software: Linux python3.6.8 Django2.0
"""

from scrapy import cmdline

cmdline.execute("scrapy crawl mm_body_s".split())
