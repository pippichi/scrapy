# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DeyaCofeedItem(scrapy.Item):

    content = scrapy.Field()


class DeyaCofeedHistoryItem(scrapy.Item):
    content = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
