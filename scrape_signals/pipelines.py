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
        data = dict(item)
        headers = {'Content-Type': 'application/json'}
        url = 'http://website_api_service_to_update_crawled_data/'

        # requests.post(url=url, headers=headers, data=json.dumps(data))\
        spider.logger.info(f'{spider.trader_id} Requested to server')
        is_success = True

        if not is_success:
            spider.hash_dict['previous_hash'] = None

        spider.write_order_hash_to_file()

        return item
