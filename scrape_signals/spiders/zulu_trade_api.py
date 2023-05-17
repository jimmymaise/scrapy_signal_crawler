from scrape_signals.base_spider import BaseSpider
from scrape_signals.items import TraderItem, SignalItem
from utils.constant import Constant


class ZuluTradeSpiderAPI(BaseSpider):
    name = Constant.ZULU_API_SPIDER_NAME
    allowed_domains = Constant.ZULU_API_ALLOWED_DOMAINS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [Constant.ZULU_API_URL_TEMPLATE.format(trader_id=self.trader_id)]

    def parse(self, response, kwargs=None):

        signals_from_crawled_web = response.json()

        trader_item = TraderItem()
        trader_item['source'] = 'zulu'
        trader_item['trader_id'] = self.trader_id
        trader_item['hash'] = self.get_item_hash(trader_item)

        trader_item['signals'] = [SignalItem({
            'signal_id': signal['id'],
            'type': signal['tradeType'],
            'size': signal['stdLotds'],
            'time': signal['dateTime'],
            'price_order': signal['entryRate'],
            'stop_loss': signal['stop'],
            'take_profit': signal['limit'],
            'market_price': signal['currentRate']
        }) for signal in signals_from_crawled_web]

        if trader_item['hash'] != self.hash_dict["previous_hash"]:
            self.logger.info(f'{self.trader_id} new hash {trader_item["hash"]}, {self.hash_dict["previous_hash"]}')
            self.hash_dict['previous_hash'] = trader_item['hash']
            yield trader_item

        else:
            self.logger.info(f'{self.trader_id} old hash {trader_item["hash"]}, Nothing to update')
            yield None
