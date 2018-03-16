from datetime import datetime
from webcrawler.settings import EXTRACTED_DATA_COLLECTION, DATABASE
from webcrawler.utils import get_urn
import pysolr


class SolrPipeline(object):
    def __init__(self, host=None,
                 collection=None):
        self.core_name = collection
        self.solr_host = host
        self.solr = pysolr.Solr('http://{0}/solr/{1}'.format(self.solr_host, collection),
                                timeout=10)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HTTPCACHE_HOST', '127.0.0.1'),
            collection=crawler.settings.get('INVANA_CRAWLER_EXTRACTION_COLLECTION', EXTRACTED_DATA_COLLECTION),
        )

    def _flatten_headers(self, obj):
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def process_item(self, item, spider):
        data = dict(item)
        data['updated'] = datetime.now()
        data['id'] = get_urn(data['url'])
        self.solr.add([data])
        return item
