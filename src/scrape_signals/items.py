# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
import json
from scrapy.item import Field


class SignalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    external_signal_id = scrapy.Field()
    symbol = scrapy.Field()
    type = scrapy.Field()
    size = scrapy.Field()
    time = scrapy.Field()
    price_order = scrapy.Field()
    stop_loss = scrapy.Field()
    take_profit = scrapy.Field()
    market_price = scrapy.Field()
    limit = scrapy.Field()


class MasterTraderItem(scrapy.Item):
    external_trader_id = Field()
    source = Field()
    signals = Field()
    hash = Field()
