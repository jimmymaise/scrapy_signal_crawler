class Constant:
    ZULU_API_URL_TEMPLATE = 'https://www.zulutrade.com/zulutrade-client/trading/api/providers/{external_trader_id}/trades/open/all'
    ZULU_API_SPIDER_NAME = 'zulu_api'
    ZULU_API_ALLOWED_DOMAINS = ['zulutrade.com']
    ZULU_API_SOURCE_NAME = 'zulu'

    CONTROLLER_BASE_URL = 'http://127.0.0.1:8000'
    MASTER_TRADER_UPSERT_TRADER_CONTROLLER_URL = CONTROLLER_BASE_URL + '/master_traders/'
