import datetime
from scrape_signals.base_spider import BaseCrawlSignalSpider
from scrape_signals.items import MasterTraderItem, SignalItem
from utils.constant import Constant
from utils.common import reverse_format_string


class ZuluTradeSpiderAPI(BaseCrawlSignalSpider):
    name = Constant.ZULU_API_BOT_TYPE_NAME
    allowed_domains = Constant.ZULU_API_ALLOWED_DOMAINS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            Constant.ZULU_API_URL_TEMPLATE.format(external_trader_id=external_trader_id)
            for external_trader_id in self.external_trader_ids
        ]

    @staticmethod
    def _normalize_symbol(symbol):
        symbol.replace("/", "")
        return symbol

    @staticmethod
    def _get_date_time(signal_time):
        if not signal_time:
            return signal_time
        return datetime.datetime.utcfromtimestamp(signal_time / 1000).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    def parse(self, response, kwargs=None):
        self.check_tor_proxy_work(response)

        external_trader_id = reverse_format_string(
            Constant.ZULU_API_URL_TEMPLATE, response.request.url
        )["external_trader_id"]
        print(response.request.url)

        signals_from_crawled_web = response.json()

        trader_item = MasterTraderItem()
        trader_item["source"] = Constant.ZULU_API_SOURCE_NAME
        trader_item["external_trader_id"] = external_trader_id
        try:
            trader_item["signals"] = [
                SignalItem(
                    {
                        "external_signal_id": str(signal.get("brokerTicket")),
                        "type": signal.get("tradeType"),
                        "size": signal.get("stdLotds"),
                        "symbol": self._normalize_symbol(signal.get("currencyName")),
                        "time": self._get_date_time(signal.get("dateTime")),
                        "price_order": signal.get("entryRate"),
                        "stop_loss": signal.get("stop"),
                        "take_profit": signal.get("limit"),
                        "market_price": signal.get("currentRate"),
                    }
                )
                for signal in signals_from_crawled_web
            ]
        except Exception as e:
            self.logger.info(
                f"{external_trader_id} Get exception {e} for {signals_from_crawled_web}"
            )
            yield None

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
