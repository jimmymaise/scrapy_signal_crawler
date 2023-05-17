from scrapy import cmdline

cmdline.execute("scrapy crawl zulu_api -a external_trader_ids=404656,7892,123".split())
