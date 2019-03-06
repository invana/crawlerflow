from __future__ import print_function
import logging
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.python import to_bytes
from scrapy.http.headers import Headers
from elasticsearch_dsl import DocType, Date, Integer, Text, connections
from datetime import datetime
from invana_bot.utils.url import get_urn, get_domain

logger = logging.getLogger(__name__)


class ESCacheStorage(object):
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
        class WebLink(DocType):
            url = Text()
            html = Text()
            headers = Text()
            status = Integer()
            created = Date()

            class Meta:
                index = self.database_name
                doc_type = self.collection_name

        return WebLink

    def __init__(self, settings):

        self.CONNECTION_URI = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "CONNECTION_URI", None)
        self.database_name = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "DATABASE_NAME", None)
        self.cache_expiry_time = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "EXPIRY_TIME", None)
        self.collection_name = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "COLLECTION_NAME", None)
        connections.create_connection(hosts=[self.CONNECTION_URI])
        self.WebLink = self.setup_collection()
        self.WebLink.init()

    def open_spider(self, spider):
        logger.debug("Using elastic cache storage with index name %(database)s" % {'database': self.CONNECTION_URI},
                     extra={'spider': spider})

    def close_spider(self, spider):
        pass

    def get_headers(self, obj):
        """
        this will convert all the headers_Server, headers_Date
        into "header": {
            "Server": "",
            "Date": ""
        }

        :param obj:
        :return:
        """
        headers = {}
        for k, v in obj.items():
            if k.startswith("headers_"):
                headers[k.replace("headers_", "")] = v

        obj['headers'] = headers
        return obj

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)

        if data is None:
            return  # not cached
        else:
            if data['status'] == 200 and data['html'] is None:
                return None

        data = self.get_headers(data)
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = bytes(data['html'], encoding="utf-8")
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def _clean_headers(self, obj):
        cleaned_object = {}
        for k, v in obj.items():
            cleaned_object[k.decode('utf-8')] = v[0].decode('utf-8')
        return cleaned_object

    def _flatten_headers(self, obj):
        flat_data = {}
        for k, v in obj.items():
            flat_data['headers_{}'.format(k)] = v
        return flat_data

    def store_response(self, spider, request, response):
        data = {
            'status': response.status,
            'domain': get_domain(response.url),
            'url': response.url,
            'html': str(response.body).lstrip("b'").strip("'")
                .replace("\\n", "")
                .replace("\\t", "")
                .replace("\\\\", "\\"),
            'created': datetime.now()
        }
        data.update(self._flatten_headers(self._clean_headers(response.headers)))
        self.WebLink(meta={'id': get_urn(response.url)}, **data).save()

    def _read_data(self, spider, request):
        try:
            return self.WebLink.get(id=get_urn(request.url)).to_dict()
        except Exception as e:
            return None

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))
