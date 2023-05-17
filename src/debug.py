import json
import click
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from utils.constant import Constant
from scrape_signals.spiders.zulu_trade_api import ZuluTradeSpiderAPI
import requests

configure_logging(install_root_handler=True)
count = 1


class CrawlHandler:
    def __init__(self, runner_name) -> None:
        self.runner_name = runner_name

    def get_trader_ids(self):
        url = Constant.CREATE_RUNNER_IF_NOT_EXIST_URL
        headers = {"Content-Type": "application/json"}
        data = {"name": self.runner_name, "crawler_type": Constant.ZULU_API_SPIDER_NAME}
        try:
            resp = requests.post(url, headers=headers, json=data)
            if resp.status_code in [requests.codes.created, requests.codes.ok]:
                assignments = resp["assignments"]
                if assignments:
                    print(assignments)

            raise Exception(
                f"Invalid status status {resp.status_code} and {resp.content}"
            )

        except Exception as e:
            self.logger.error(e)

    def run_crawl(self):
        """
        Run a spider within Twisted. Once it completes,
        schedule the next spider to run immediately.
        """

        import os

        print(os.getcwd())
        with open("./trader_ids.json") as content:
            trader_ids = json.load(content)
        runner = CrawlerRunner(get_project_settings())

        ab = self.get_trader_ids()
        global count
        count += 1
        print(f"AAAAAAAAAAAAAAAAAAAAA-AAAAAAAAAAAAAAAAAAAAA{count}")
        deferred = runner.crawl(
            ZuluTradeSpiderAPI, external_trader_ids=trader_ids["trader_ids"]
        )
        deferred.addCallback(lambda _: reactor.callLater(1, self.run_crawl))
        return deferred

    def start(self):
        self.run_crawl()
        reactor.run()


@click.command()
@click.option("--runner-id", default=1, help="Name Runner.")
def start_runner(runner_id):
    """Simple program that greets NAME for a total of COUNT times."""
    CrawlHandler(runner_id).start()


if __name__ == "__main__":
    start_runner()
