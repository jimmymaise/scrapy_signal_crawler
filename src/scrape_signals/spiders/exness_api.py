import datetime
from scrape_signals.base_spider import BaseCrawlSignalSpider
from scrape_signals.items import MasterTraderItem, SignalItem
from utils.constant import Constant
from utils.common import reverse_format_string


class ExnessSpiderAPI(BaseCrawlSignalSpider):
    name = Constant.EXNESS_API_BOT_TYPE_NAME
    allowed_domains = Constant.EXNESS_API_ALLOWED_DOMAINS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            Constant.EXNESS_API_URL_TEMPLATE.format(
                external_trader_id=external_trader_id
            )
            for external_trader_id in self.external_trader_ids
        ]

    @staticmethod
    def _normalize_symbol(symbol):
        if symbol.endswith("m"):
            return symbol[:-1]
        return symbol

    def parse(self, response, kwargs=None):
        self.check_tor_proxy_work(response)
        external_trader_id = reverse_format_string(
            Constant.EXNESS_API_URL_TEMPLATE, response.request.url
        )["external_trader_id"]

        signals_from_crawled_web = response.json()["result"]

        trader_item = MasterTraderItem()
        trader_item["source"] = Constant.EXNESS_API_SOURCE_NAME
        trader_item["external_trader_id"] = external_trader_id

        trader_item["signals"] = [
            SignalItem(
                {
                    "external_signal_id": str(signal.get("order_id")),
                    "type": signal.get("trade_type"),
                    "size": signal.get("size"),
                    "symbol": self._normalize_symbol(signal.get("symbol")),
                    "time": signal.get("open_datetime"),
                    "price_order": signal.get("open_price"),
                    "stop_loss": None,
                    "take_profit": None,
                    "market_price": signal.get("current_price"),
                }
            )
            for signal in signals_from_crawled_web
        ]

        previous_hash = self.load_previous_order_hash_for_trader(external_trader_id)
        trader_item["hash"] = self.get_item_hash(trader_item)

        if trader_item["hash"] != previous_hash:
            self.logger.info(
                f'{external_trader_id} new hash {trader_item["hash"]}, {previous_hash}'
            )
            yield trader_item

        else:
            self.logger.info(
                f'{external_trader_id} old hash {trader_item["hash"]}, Nothing to update'
            )
            yield None
