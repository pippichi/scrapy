#!/usr/bin/env python
# -*- encoding: utf-8 -*-   
# @Time    :  2020/8/6 上午11:19 
# @Author  :  TCL
from scrapy import cmdline
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# cmdline.execute(["scrapy", "crawl", "spider_5"])
# cmdline.execute(["scrapy", "crawl", "spider_5_history"])
# cmdline.execute(["scrapy", "crawl", "spider_6"])
# cmdline.execute(["scrapy", "crawl", "spider_6_history"])
# cmdline.execute(["scrapy", "crawl", "spider_7"])
cmdline.execute(["scrapy", "crawl", "spider_7_history"])
# cmdline.execute(["scrapy", "crawl", "spider_8_9"])
