MONGODB_DEFAULTS = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
}

ELASTICSEARCH_DEFAULTS = {
    'ITEM_PIPELINES': {'invana_bot.pipelines.elasticsearch.ElasticSearchPipeline': 1},
    'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
}

KEYWORD_CRAWLER_DEFAULTS = {

    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "keywords_data"
        }
    }
}

FEEDS_CRAWLER_DEFAULTS = {

    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "feeds_data"
        }
    }
}

WEBSITE_CRAWLER_DEFAULTS = {

    'INVANA_BOT_SETTINGS': {
        'HTTPCACHE_STORAGE_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_cache_db",
            'COLLECTION_NAME': "web_link",
            "EXPIRY_TIME": 3600
        },
        'ITEM_PIPELINES_SETTINGS': {
            'DATABASE_URI': "127.0.0.1",
            'DATABASE_NAME': "crawler_data",
            'COLLECTION_NAME': "website_data"
        }
    }
}
