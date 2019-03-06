DEFAULT_SETTINGS = {
    'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
    'HTTPCACHE_ENABLED': True,
    'TELNETCONSOLE_PORT': None,
    'ITEM_PIPELINES': {'invana_bot.storages.mongodb.MongoDBPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",

    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'CONNECTION_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'CONNECTION_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "website_data"
        }
    }

}
