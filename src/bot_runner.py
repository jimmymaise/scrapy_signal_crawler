import click
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from utils.constant import Constant
from scrape_signals.spiders.zulu_trade_api import ZuluTradeSpiderAPI
import requests
from utils.common import SimpleCache
import datetime
import time

configure_logging(install_root_handler=True)
trader_id_cache = None

cache = SimpleCache()


class CrawlHandler:
    def __init__(self, runner_name) -> None:
        self.runner_name = runner_name

    def get_trader_ids(self):
        url = Constant.CREATE_RUNNER_IF_NOT_EXIST_URL
        headers = {"Content-Type": "application/json"}
        data = {"name": self.runner_name, "crawler_type": Constant.ZULU_API_SPIDER_NAME}
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
            print(
                f"Cannot get crawl assignments as {e}. Retry after {Constant.RETRY_TIME_MS} seconds"
            )
            time.sleep(Constant.RETRY_TIME_MS)

    def run_crawl(self):
        """
        Run a spider within Twisted. Once it completes,
        schedule the next spider to run immediately.
        """
        global cache
        runner = CrawlerRunner(get_project_settings())
        trader_ids = cache.get("trader_ids")

        while not trader_ids:
            trader_ids = self.get_trader_ids()

        cache.set("trader_ids", trader_ids, 300)
        print(f"[{datetime.datetime.now()}] Crawling with {trader_ids}")

        deferred = runner.crawl(ZuluTradeSpiderAPI, external_trader_ids=trader_ids)
        deferred.addCallback(lambda _: reactor.callLater(1, self.run_crawl))
        return deferred

    def start(self):
        self.run_crawl()
        reactor.run()


@click.command()
@click.option("--runner-name", help="Name Runner.", required=True)
def start_runner(runner_name):
    """Simple program that greets NAME for a total of COUNT times."""
    print(f"########## Runner {runner_name} has been started ############")
    CrawlHandler(runner_name).start()


if __name__ == "__main__":
    start_runner()
    # import os
    # pid = os.getpid()
    # start_runner(["--runner-name", f"trader_test_debug_{pid}"])
