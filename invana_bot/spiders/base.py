from scrapy.spiders import CrawlSpider
from scrapy.http import Request

import os


class WebCrawlerBase(CrawlSpider):
    """

    TODO - document why we need this as base method.

    """

    spider_id = None
    spider_config = None
    spider_data_storage = None
    manifest = {}

    # @property
    # def data_storage(self):
    #     return self.spider_config.get("data_storage")

    @staticmethod
    def get_default_storage(settings=None, spider_config=None):
        data_storages = settings.get("DATA_STORAGES", [])
        default_storage = None
        for data_storage in data_storages:
            if data_storage.get("storage_id") == spider_config.get("storage_id", "default"):
                return data_storage
        return default_storage

    @staticmethod
    def prepare_data_for_yield(data=None, collection_name=None, storage_id="default"):
        return {
            "_data_storage_id": storage_id,
            "_data_storage_collection_name": collection_name,
            "_data": data
        }

    def _build_request(self, rule, link):
        headers = {}
        user_agent_header = os.environ.get("WCP_REQUEST_HEADERS_USER_AGENT")
        if user_agent_header:
            headers = {"User-Agent": user_agent_header}
        r = Request(url=link.url, headers=headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r
