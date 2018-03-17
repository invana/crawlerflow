from __future__ import print_function
import logging
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.python import to_bytes, to_unicode, garbage_collect
import pymongo
from scrapy.http.headers import Headers
from webcrawler.settings import DATA_COLLECTION, DATABASE
from webcrawler.utils.url import get_urn, get_domain

logger = logging.getLogger(__name__)


class MongoDBCacheStorage(object):
    """
    should set HTTPCACHE_MONGODB_DATABASE in the settings.py


    """
    COLLECTION_NAME = DATA_COLLECTION

    def __init__(self, settings):
        self.database = settings.get('HTTPCACHE_MONGODB_DATABASE', DATABASE)
        self.database_host = settings.get('HTTPCACHE_HOST', '127.0.0.1')

        self.database_port = settings.get('HTTPCACHE_MONGODB_PORT', 27017)

        auth = {
            "username": settings.get('HTTPCACHE_MONGODB_USERNAME', ''),
            "password": settings.get('HTTPCACHE_MONGODB_PASSWORD', '')
        }
        if auth.get('username'):
            self.db_client = pymongo.MongoClient(self.database_host, **auth)
        else:
            self.db_client = pymongo.MongoClient(self.database_host, )
        self.db = self.db_client[self.database]

        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')

    def open_spider(self, spider):
        logger.debug("Using mongodb cache storage with database name %(database)s" % {'database': self.database},
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
        self.db[self.COLLECTION_NAME].insert_one(data)

    def _read_data(self, spider, request):
        return self.db[self.COLLECTION_NAME].find_one({'url': request.url})

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))
