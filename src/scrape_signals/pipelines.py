# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
import json


class SendAPIPipeline:
    def process_item(self, item, spider):
        print('Sending item to controller')
        updated_hash = spider.send_crawled_signals_data_to_controller(item)
        spider.write_order_hash_to_file(item['external_trader_id'], updated_hash)
        return item
