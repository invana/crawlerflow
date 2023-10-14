

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"

DEFAULT_SETTINGS_OVERRIDES = {
    'LOG_LEVEL' : "INFO",
    'RETRY_TIMES' : 5,
    'COMPRESSION_ENABLED': True,
    'HTTPCACHE_ENABLED': False,
    'USER_AGENT' : DEFAULT_USER_AGENT,
 
    'ITEM_PIPELINES': {
        'web_scraper.pipelines.MetadataPipeline': 0,
        'web_scraper.pipelines.MongoDBPipeline': 1,
        # 'web_scraper.pipelines.JsonWriterPipeline': 2,
    },
    'DOWNLOADER_MIDDLEWARES': {
        "web_scraper.downloaders.RequestsDownloaderMiddleware": 501,
    },
    'MONGO_URI': "mongodb://root:example@localhost:27017",
    'MONGO_DATABASE': "web_scraper",
    'MONGO_DEFAULT_COLLECTION': 'scraped_items'
}