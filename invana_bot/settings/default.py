DEFAULT_SETTINGS_BASE = {
    'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
    'HTTPCACHE_ENABLED': True,
    'TELNETCONSOLE_PORT': [6023, 6073],

}

MONGODB_SETTINGS = {
    'ITEM_PIPELINES': {'invana_bot.core.storages.mongodb.MongoDBPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.core.httpcache.mongodb.MongoDBCacheStorage",

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

ELASTICSEARCH_SETTINGS = {
    'ITEM_PIPELINES': {'invana_bot.core.storages.elasticsearch.ElasticSearchPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.core.httpcache.elasticsearch.ESCacheStorage",

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

DEFAULT_SETTINGS = {}
DEFAULT_SETTINGS.update(DEFAULT_SETTINGS_BASE)
DEFAULT_SETTINGS.update(MONGODB_SETTINGS)
