from webcrawler.utils import example_config
from webcrawler.parser import crawler

common_settings = {
    'COMPRESSION_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'INVANA_CRAWLER_COLLECTION': "weblinks",
    'INVANA_CRAWLER_EXTRACTION_COLLECTION': "weblinks_extracted_data",
    'LOG_LEVEL': 'INFO'
}

mongodb_settings = {
    'PIPELINE_MONGODB_DATABASE': "crawler_data",
    'ITEM_PIPELINES': {'webcrawler.pipelines.mongodb.MongoDBPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler.httpcache.mongodb.MongoDBCacheStorage",
    'HTTPCACHE_MONGODB_DATABASE': "crawler_data",
    "HTTPCACHE_MONGODB_PORT": 27017,
}

es_settings = {
    'PIPELINE_ES_DATABASE': "crawlers",
    'ITEM_PIPELINES': {'webcrawler.pipelines.elasticsearch.ElasticsearchPipeline': 1},

    'HTTPCACHE_STORAGE': "webcrawler.httpcache.elasticsearch.ESCacheStorage",
}

common_settings.update(mongodb_settings)
# common_settings.update(es_settings)
print(common_settings)

if __name__ == '__main__':
    crawler(config=example_config, settings=common_settings)
