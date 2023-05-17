import datetime
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
        self.external_trader_ids = kwargs["external_trader_ids"] = kwargs[
            "external_trader_ids"
        ].split(",")

        self.is_use_tor = kwargs.get("is_use_tor")

        super().__init__(*args, **kwargs)

        self.data_path = f"./data/{self.name}"
        self.hash_path_folder = f"{self.data_path}/hash/"
        self.pid = os.getpid()
        self.logger.info(
            f"Spider {self.name} with trader ids:{self.external_trader_ids}  is running with PID {self.pid}"
            f" with flag is_use_tor {self.is_use_tor}"
        )

    def check_tor_proxy_work(self, response):
        if self.is_use_tor:
            self.logger.info(f"Using tor IP {response.request.meta.get('tor_ipaddress')}")

    def get_hash_file_path(self, trader_id):
        return f"{self.hash_path_folder}/{trader_id}.json"

    def load_previous_order_hash_for_trader(self, trader_id):
        hash_file_path = self.get_hash_file_path(trader_id)
        if not pathlib.Path(hash_file_path).is_file():
            # creating a new directory called pythondirectory
            pathlib.Path(self.hash_path_folder).mkdir(parents=True, exist_ok=True)
            return None

        with open(hash_file_path) as content:
            return json.load(content)["previous_hash"]

    def write_order_hash_to_file(self, trader_id, new_hash):
        with open(self.get_hash_file_path(trader_id), "w") as content:
            json.dump(
                {
                    "previous_hash": new_hash,
                    "last_updated": str(datetime.datetime.now()),
                },
                content,
            )

    def send_crawled_signals_data_to_controller(
            self, master_trader_with_crawled_signals_data
    ):
        data = dict(master_trader_with_crawled_signals_data)
        external_trader_id = data["external_trader_id"]
        headers = {"Content-Type": "application/json"}
        try:
            resp = requests.post(
                url=Constant.MASTER_TRADER_UPSERT_TRADER_CONTROLLER_URL,
                headers=headers,
                data=self.encoder.encode(data),
                timeout=Constant.DEFAULT_REQUEST_TIME_OUT
            )
        except Exception as e:
            self.logger.error(f"Error when pushing the result\n {e} ")
            return None

        updated_hash = None

        if resp.status_code in [requests.codes.created, requests.codes.ok]:
            self.logger.info(
                f"[SUCCESS, code={resp.status_code}] Post crawled signals of {external_trader_id} to server"
            )

            updated_hash = master_trader_with_crawled_signals_data["hash"]
        else:
            self.logger.error(
                f"[FAILED, code={resp.status_code}] Post crawled signals of {external_trader_id} to server."
                f" Response {resp.content}"
            )

        return updated_hash

    def parse(self, response, kwargs=None):
        pass

    @staticmethod
    def get_item_hash(content):
        return str(hashlib.md5(str(content).encode()).hexdigest())
