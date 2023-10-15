

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"

DEFAULT_SETTINGS_OVERRIDES = {
    'LOG_LEVEL' : "INFO",
    'RETRY_TIMES' : 5,
    'COMPRESSION_ENABLED': True,
    'HTTPCACHE_ENABLED': False,
    'USER_AGENT' : DEFAULT_USER_AGENT,
 
    'ITEM_PIPELINES': {
        'crawlerflow.pipelines.MetadataPipeline': 0,
        'crawlerflow.pipelines.MongoDBPipeline': 1,
        # 'crawlerflow.pipelines.JsonWriterPipeline': 2,
    },
    'DOWNLOADER_MIDDLEWARES': {
        "crawlerflow.downloaders.RequestsDownloaderMiddleware": 501,
    },
    
    'STORAGE_MONGO_URI': "mongodb://root:example@localhost:27017",
    'STORAGE_MONGO_DATABASE': "crawlerflow",
    'STORAGE_MONGO_DEFAULT_COLLECTION': 'scraped_items'
}