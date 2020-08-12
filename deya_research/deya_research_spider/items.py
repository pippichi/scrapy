# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DeyaResearchSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Spider1516Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 规格（如 T30S/M800E 等）
    specificationName = scrapy.Field()
    # 标准（如 拉丝/注塑 等）
    standard = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 地区
    regionName = scrapy.Field()

class Spider17Item(scrapy.Item):
    # 合约类型
    contract = scrapy.Field()
    # 名次
    rank = scrapy.Field()
    # 类型（成交/多头持仓/空头持仓/仓单）
    type = scrapy.Field()
    # 会员简称
    memberName = scrapy.Field()
    # 数据值（成交量/持买单量/持卖单量）
    value = scrapy.Field()
    # 日期
    date = scrapy.Field()
