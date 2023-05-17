import os
import json
import scrapy
import pathlib
import hashlib
from utils.constant import Constant
from scrapy.utils.serialize import ScrapyJSONEncoder
import requests


class BaseCrawlSignalSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        self.encoder = ScrapyJSONEncoder()
        self.external_trader_id = kwargs['external_trader_id']
        super().__init__(*args, **kwargs)

        self.data_path = f'./data/{self.name}'
        self.hash_path = f'{self.data_path}/hash/{self.external_trader_id}.json'
        self.hash_dict = self.load_previous_order_hash_for_trader()
        self.pid = os.getpid()
        self.logger.info(f"Spider {self.name} with trader id:{self.external_trader_id}  is running with PID {self.pid}")

    def load_previous_order_hash_for_trader(self):
        if not pathlib.Path(self.hash_path).is_file():
            # creating a new directory called pythondirectory
            pathlib.Path(self.hash_path).parent.mkdir(parents=True, exist_ok=True)
            return {'previous_hash': None}

        with open(self.hash_path) as content:
            return json.load(content)

    def write_order_hash_to_file(self):
        with open(self.hash_path, 'w') as content:
            json.dump(self.hash_dict, content)

    def send_crawled_signals_data_to_controller(self, master_trader_with_crawled_signals_data):
        data = dict(master_trader_with_crawled_signals_data)
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url=Constant.MASTER_TRADER_UPSERT_TRADER_CONTROLLER_URL
                             , headers=headers, data=self.encoder.encode(data))

        if resp.status_code in [requests.codes.created, requests.codes.ok]:
            self.logger.info(
                f'[SUCCESS, code={resp.status_code}] Post crawled signals of {self.external_trader_id} to server')
        else:
            self.logger.error(
                f'[FAILED, code={resp.status_code}] Post crawled signals of {self.external_trader_id} to server.'
                f' Response {resp.content}')
            self.hash_dict['previous_hash'] = None

    def parse(self, response, kwargs=None):
        pass

    @staticmethod
    def get_item_hash(content):
        return str(hashlib.md5(str(content).encode()).hexdigest())
