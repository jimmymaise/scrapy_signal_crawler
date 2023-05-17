import click
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from utils.constant import Constant
from scrape_signals.spiders.zulu_trade_api import ZuluTradeSpiderAPI
from scrape_signals.spiders.exness_api import ExnessSpiderAPI

import requests
from utils.common import SimpleCache
import datetime
import time
import pathlib
import os

configure_logging(install_root_handler=True)
os.environ["SCRAPY_SETTINGS_MODULE"] = "scrape_signals.settings"


class CrawlHandler:
    def __init__(self, runner_name, bot_type, is_use_tor=False) -> None:
        self.runner_name = runner_name
        self.bot_type = bot_type
        self.cache = SimpleCache()
        self.is_use_tor = is_use_tor
        self.bot_setting = get_project_settings()
        if self.is_use_tor:
            self.bot_setting.update(Constant.TOR_PROXY_SETTING)

        match bot_type:
            case Constant.ZULU_API_BOT_TYPE_NAME:
                self.spider_class = ZuluTradeSpiderAPI

            case Constant.EXNESS_API_BOT_TYPE_NAME:
                self.spider_class = ExnessSpiderAPI

            case _:
                raise Exception(f"Invalid bot type {bot_type}")

    def get_trader_ids(self):
        url = Constant.CREATE_RUNNER_IF_NOT_EXIST_URL
        headers = {"Content-Type": "application/json"}
        data = {"name": self.runner_name, "crawler_type": self.bot_type}
        print(data)
        error = ""
        try:
            resp = requests.post(url, headers=headers, json=data)
            if resp.status_code in [requests.codes.created, requests.codes.ok]:
                assignments = resp.json()["assignments"]
                if assignments:
                    return ",".join(
                        [
                            assignment["master_trader"]["external_trader_id"]
                            for assignment in assignments
                        ]
                    )
                error = "Server responds `no assignments`"
            else:
                error = f"Invalid status status {resp.status_code} and {resp.content}"

            raise Exception(error)

        except Exception as e:
            print(f"Cannot get crawl assignments as {e}.")

    def get_trader_id_by_cache(self):
        trader_ids = self.cache.get("trader_ids")

        while not trader_ids:
            trader_ids = self.get_trader_ids()
            if trader_ids:
                print(f"Set Cache: {time.sleep(Constant.RETRY_TIME_MS)} seconds")
                self.cache.set(
                    "trader_ids", trader_ids, Constant.CACHE_TIME_TO_GET_ASSIGNMENT_SEC
                )
            else:
                print(f"Retry after {time.sleep(Constant.RETRY_TIME_MS)}")
                time.sleep(Constant.RETRY_TIME_MS)

        return trader_ids

    def run_crawl(self):
        """
        Run a spider within Twisted. Once it completes,
        schedule the next spider to run immediately.
        """
        runner = CrawlerRunner(self.bot_setting)
        trader_ids = self.cache.get("trader_ids")

        while not trader_ids:
            trader_ids = self.get_trader_ids()
            if trader_ids:
                self.cache.set(
                    "trader_ids", trader_ids, Constant.CACHE_TIME_TO_GET_ASSIGNMENT_SEC
                )
        print(f"[{datetime.datetime.now()}] Crawling with {trader_ids}")

        deferred = runner.crawl(
            self.spider_class,
            external_trader_ids=trader_ids,
            is_use_tor=self.is_use_tor,
        )
        deferred.addCallback(lambda _: reactor.callLater(1, self.run_crawl))
        return deferred

    def start(self):
        self.run_crawl()
        reactor.run()


@click.command()
@click.option("--bot-type", help="Name Bot.", required=True)
@click.option("--runner-name", help="Name Runner.", required=True)
@click.option(
    "--tor",
    "is_use_tor",
    is_flag=True,
    default=False,
    help="Read the full file (default).",
)
def start_runner(runner_name, bot_type, is_use_tor):
    """Simple program that greets NAME for a total of COUNT times."""
    print(f"########## Runner {runner_name} has been started ############")
    CrawlHandler(runner_name, bot_type, is_use_tor).start()


if __name__ == "__main__":
    # start_runner()
    # import os

    # pid = os.getpid()
    start_runner(["--runner-name", f"trader_test_debug", "--bot-type", "exness_api", "--tor"])
