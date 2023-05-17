import os
import json
import scrapy
import pathlib
import hashlib


class BaseSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        self.trader_id = kwargs['trader_id']
        super().__init__(*args, **kwargs)

        self.data_path = f'./data/{self.name}'
        self.hash_path = f'{self.data_path}/hash/{self.trader_id}.json'
        self.hash_dict = self.load_previous_order_hash_for_trader()
        self.pid = os.getpid()
        self.logger.info(f"Spider {self.name} with trader id:{self.trader_id}  is running with PID {self.pid}")

    def load_previous_order_hash_for_trader(self):
        if not pathlib.Path(self.hash_path).is_file():
            return

        with open(self.hash_path) as content:
            return json.load(content)

    def write_order_hash_to_file(self):
        with open(self.hash_path, 'w') as content:
            json.dump(self.hash_dict, content)

    def parse(self, response, kwargs=None):
        pass

    @staticmethod
    def get_item_hash(content):
        return str(hashlib.md5(str(content).encode()).hexdigest())
