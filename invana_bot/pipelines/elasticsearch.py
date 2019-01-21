from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Text, connections
from invana_bot.settings import EXTRACTED_DATA_COLLECTION, DATABASE
from invana_bot.utils.url import get_urn


class WebLinkExtracted(DocType):
    url = Text()
    body = Text()
    headers = Text()
    status = Integer()
    created = Date()

    class Meta:
        index = DATABASE
        doc_type = EXTRACTED_DATA_COLLECTION


class ElasticSearchPipeline(object):
    def __init__(self, database_uri=None,
                 database_name=None,
                 collection_name=None):
        print ("++++++",database_name, collection_name, collection_name)
        self.database_uri = database_uri
        self.collection_name = collection_name
        connections.create_connection(hosts=[self.database_uri])
        WebLinkExtracted.init()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_uri=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get('DATABASE_URI'),
            database_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_NAME'),
            collection_name=crawler.settings.get('INVANA_BOT_SETTINGS').get('ITEM_PIPELINES_SETTINGS').get(
                'DATABASE_COLLECTION')
        )

    def _flatten_headers(self, obj):  # TODO -may be not using !!
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def process_item(self, item, spider):
        data = dict(item)
        data['updated'] = datetime.now()
        WebLinkExtracted(meta={'id': get_urn(data['url'])}, **data).save()
        return item
