import json

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from scrape_signals.spiders.zulu_trade_api import ZuluTradeSpiderAPI

configure_logging(install_root_handler=True)


def run_crawl():
    """
    Run a spider within Twisted. Once it completes,
    schedule the next spider to run immediately.
    """
    with open('./trader_ids.json') as content:
        trader_ids = json.load(content)
    runner = CrawlerRunner(get_project_settings())
    deferred = runner.crawl(ZuluTradeSpiderAPI, external_trader_ids=trader_ids['trader_ids'])
    deferred.addCallback(lambda _: reactor.callLater(1, run_crawl))
    return deferred


run_crawl()
reactor.run()
