from __future__ import print_function
import logging
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.python import to_bytes
import pymongo
from scrapy.http.headers import Headers
from invana_bot.utils.url import get_domain

logger = logging.getLogger(__name__)


class MongoDBCacheStorage(object):
    """
    should set INVANA_BOT_SETTINGS in the default.py

    pipeline_settings = {
        'ITEM_PIPELINES': {'invana_bot.storages.mongodb.MongoDBPipeline': 1},
        'HTTPCACHE_STORAGE': "invana_bot.httpcache.mongodb.MongoDBCacheStorage",
    }

    mongodb_settings = {
        'INVANA_BOT_SETTINGS': {
            'HTTPCACHE_STORAGE_SETTINGS': {
                'CONNECTION_URI': "mongodb://127.0.0.1",
                'DATABASE_NAME': "crawler_cache_db",
                'COLLECTION_NAME': "web_link",
                "EXPIRY_TIME": 3600
            },
            'ITEM_PIPELINES_SETTINGS': {
                'CONNECTION_URI': "mongodb://127.0.0.1",
                'DATABASE_NAME': "crawler_data",
                'COLLECTION_NAME': "crawler_feeds_data"
            }
        }
    }


    """

    def __init__(self, settings):
        self.CONNECTION_URI = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "CONNECTION_URI", None)
        self.database_name = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "DATABASE_NAME", None)
        self.cache_expiry_time = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "EXPIRY_TIME", None)
        self.collection_name = settings.get('INVANA_BOT_SETTINGS', {}).get('HTTPCACHE_STORAGE_SETTINGS', {}).get(
            "COLLECTION_NAME", None)
        self.db_client = pymongo.MongoClient(self.CONNECTION_URI)
        self.db = self.db_client[self.database_name]

    def open_spider(self, spider):
        logger.debug("Using mongodb cache storage with database name %(database)s" % {'database': self.database_name},
                     extra={'spider': spider})

    def close_spider(self, spider):
        pass

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)
        if data is None:
            return  # not cached
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = data['html']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def _clean_headers(self, obj):
        cleaned_object = {}
        for k, v in obj.items():
            cleaned_object[k.decode('utf-8')] = v[0].decode('utf-8')
        return cleaned_object

    def store_response(self, spider, request, response):
        data = {
            'status': response.status,
            'domain': get_domain(response.url),
            'url': response.url,
            'headers': self._clean_headers(response.headers),
            'html': response.body,
        }
        self.db[self.collection_name].insert_one(data)

    def _read_data(self, spider, request):
        return self.db[self.collection_name].find_one({'url': request.url})

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))
