import os


class Constant:
    ZULU_API_URL_TEMPLATE = "https://www.zulutrade.com/zulutrade-client/trading/api/providers/{external_trader_id}/trades/open/all"
    ZULU_API_BOT_TYPE_NAME = "zulu_api"
    ZULU_API_ALLOWED_DOMAINS = ["zulutrade.com"]
    ZULU_API_SOURCE_NAME = "zulu"

    EXNESS_API_URL_TEMPLATE = "https://social-trading.exness.com/st/v1/managers/accounts/{external_trader_id}/open-trades/"
    EXNESS_API_BOT_TYPE_NAME = "exness_api"
    EXNESS_API_ALLOWED_DOMAINS = ["exness.com"]
    EXNESS_API_SOURCE_NAME = "exness"

    CONTROLLER_BASE_URL = os.getenv("CONTROLLER_BASE_URL", "http://localhost:8000")
    MASTER_TRADER_UPSERT_TRADER_CONTROLLER_URL = (
            CONTROLLER_BASE_URL + "/master_traders/"
    )
    CREATE_RUNNER_IF_NOT_EXIST_URL = CONTROLLER_BASE_URL + "/crawl_runners/"
    RETRY_TIME_SECONDS = 60
    RETRY_WHEN_CRAWL_ERROR_SECONDS = 30
    RETRY_WHEN_CRAWL_COMPLETE_SECONDS = 1
    CACHE_TIME_TO_GET_ASSIGNMENT_SEC = 30

    TOR_PROXY_SETTING = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 0.5,
        "TOR_IP_ROTATOR_ENABLED": True,
        "TOR_IP_ROTATOR_CHANGE_AFTER": 2,  # number of requests made on the same Tor's IP address
        "TOR_IP_ROTATOR_ALLOW_REUSE_IP_AFTER": 10,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
            "scrapy_tor_rotation.middlewares.TorProxyMiddleware": 100,
        },
    }
    DEFAULT_REQUEST_TIME_OUT = 30
