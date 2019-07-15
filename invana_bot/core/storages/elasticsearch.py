from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Text, connections
from invana_bot.utils.url import get_urn


class ElasticSearchPipeline(object):
    """


    pipeline_settings = {
        'ITEM_PIPELINES': {'invana_bot.storages.elasticsearch.ElasticSearchPipeline': 1},
        'HTTPCACHE_STORAGE': "invana_bot.httpcache.elasticsearch.ESCacheStorage",
    }

    es_settings = {
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
                'COLLECTION_NAME': "crawler_feeds_data"
            }
        }
    }

    """

    def setup_collection(self):
        class WebLinkExtracted(DocType):
            url = Text()
            body = Text()
            headers = Text()
            status = Integer()
            created = Date()

            class Meta:
                index = self.database_name
                doc_type = self.collection_name

        return WebLinkExtracted

    def __init__(self, connection_uri=None,
                 database_name=None,
                 collection_name=None):
        self.connection_uri = connection_uri
        self.database_name = database_name
        self.collection_name = collection_name
        connections.create_connection(hosts=[self.connection_uri])
        self.WebLinkExtracted = self.setup_collection()
        self.WebLinkExtracted.init()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connection_uri=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get('CONNECTION_URI'),
            database_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_NAME'),
            collection_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'COLLECTION_NAME')
        )

    def _flatten_headers(self, obj):  # TODO -may be not using !!
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def process_item(self, item, spider):
        data = dict(item)
        data['updated'] = datetime.now()
        self.WebLinkExtracted(meta={'id': get_urn(data['url'])}, **data).save()
        return item
