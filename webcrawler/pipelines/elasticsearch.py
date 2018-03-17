from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Text, connections
from webcrawler.settings import EXTRACTED_DATA_COLLECTION, DATABASE
from webcrawler.utils.url import get_urn


class WebLinkExtracted(DocType):
    url = Text()
    body = Text()
    headers = Text()
    status = Integer()
    created = Date()

    class Meta:
        index = DATABASE
        doc_type = EXTRACTED_DATA_COLLECTION


class ElasticsearchPipeline(object):
    def __init__(self, host=None,
                 collection=None):
        self.database_host = host
        self.collection = collection
        connections.create_connection(hosts=[host])
        WebLinkExtracted.init()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HTTPCACHE_HOST', '127.0.0.1'),
            collection=crawler.settings.get('INVANA_CRAWLER_EXTRACTION_COLLECTION', "weblinks_extracted_data"),
        )

    def _flatten_headers(self, obj):
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def process_item(self, item, spider):
        data = dict(item)
        data['updated'] = datetime.now()
        WebLinkExtracted(meta={'id': get_urn(data['url'])}, **data).save()
        return item
