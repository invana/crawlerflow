from __future__ import print_function
import logging
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.python import to_bytes
from scrapy.http.headers import Headers
from datetime import datetime
from webcrawler.settings import DATA_COLLECTION, DATABASE
from webcrawler.utils.url import get_urn, get_domain
import pysolr

logger = logging.getLogger(__name__)


class SolrCacheStorage(object):
    """
    should set HTTPCACHE_ES_DATABASE in the settings.py


    """
    COLLECTION_NAME = "weblinks"

    solr_date_fields = [
        'headers_Last-Modified',
        'headers_Expires',
        'headers_Date',
        'created'
    ]

    solr_int_fields = [
        'status',
        'headers_X-Cache-Hits'
    ]

    solr_content_fields = [

        'description',
        'content'
    ]

    def __init__(self, settings):
        self.core_name = settings['INVANA_CRAWLER_COLLECTION']
        self.solr_host = settings.get('HTTPCACHE_HOST', '127.0.0.1:8983')

        self.solr = pysolr.Solr('http://{0}/solr/{1}'.format(self.solr_host, DATA_COLLECTION),
                                timeout=10)
        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')

    def open_spider(self, spider):
        logger.debug("Using solr cache storage with core name %(core_name)s" % {'core_name': self.core_name},
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
                headers[k.replace("headers_", "").rstrip("_s").rstrip("_i").rstrip("_dt")] = v

        obj['headers'] = headers
        return obj

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)

        if data is None:
            return  # not cached
        else:
            if data['status_i'] == 200 and data['html'] is None:
                return None

        data = self.get_headers(data)
        url = data['url_s']
        status = data['status_i']
        headers = Headers(data['headers'])
        body = bytes(data['html'][0], encoding="utf-8")
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

    def handle_date(self, v):
        new_v = None
        try:
            if type(v) == str:
                if "+" in v:
                    v = v.split("+")[0].strip()
                else:
                    v = v.replace("GMT", "").strip()
                new_v = datetime.strptime(v, '%a, %d %b %Y %H:%M:%S')
            else:
                new_v = v
        except Exception as e:
            pass
        return new_v

    def map_to_solr_datatypes(self, data):
        mapped_data = {}
        for k, v in data.items():
            if k in self.solr_date_fields:
                new_v = self.handle_date(v)
                if new_v:
                    mapped_data["{}_dt".format(k)] = new_v

            elif k in self.solr_int_fields:
                mapped_data["{}_i".format(k)] = v
            else:
                if k in self.solr_content_fields:
                    mapped_data["{}".format(k)] = v
                else:
                    mapped_data["{}_s".format(k)] = v

        if "html_s" in mapped_data:
            mapped_data['html'] = mapped_data['html_s']
            del mapped_data['html_s']
        return mapped_data

    def clean_str(self, url):
        return url.replace(".", "-").replace(":", "-")

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

        data = self.map_to_solr_datatypes(data=data)
        data['id'] = self.clean_str(get_urn(response.url))

        self.solr.add([data])

    def _read_data(self, spider, request):
        try:
            result = self.solr.search(q='id:{}'.format(self.clean_str(get_urn(request.url))))
            doc = result.docs[0]
            return doc
        except Exception as e:
            return None

    def _request_key(self, request):
        return to_bytes(request_fingerprint(request))
