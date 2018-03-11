from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Text, connections
from webcrawler.settings import EXTRACTED_DATA_COLLECTION, DATABASE


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
                 database=None,
                 collection=None):
        self.database = database
        self.database_host = host
        connections.create_connection(hosts=[host])
        WebLinkExtracted.init()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('PIPELINE_ES_HOST', '127.0.0.1'),
            database=crawler.settings.get('PIPELINE_ES_DATABASE', 'crawler_data'),
            collection=crawler.settings.get('INVANA_CRAWLER_EXTRACTION_COLLECTION', "weblinks"), # TODO - not using
        )

    def _flatten_headers(self, obj):
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def process_item(self, item, spider):
        data = dict(item)
        data['updated_at'] = datetime.now()

        # data.update(self._flatten_headers(data))  # TODO - flatten the data also for
        WebLinkExtracted(meta={'id': data['url']}, **data).save()

        return item
