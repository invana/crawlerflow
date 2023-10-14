import scrapy
import datetime
import abc
from slugify import slugify
from web_scraper.utils import get_domain, get_urn, generate_uuid
import requests
import logging
from ..request import CrawlRequest

class SpiderBase(scrapy.Spider):

    name: str = "default-spider-name"
    start_urls: list = []
    crawl_requests: list[CrawlRequest] = []
    downloader: str = "default"
    spider_type: str = "Spider"
    custom_settings: dict = {}
    default_extractor: dict = None  # this will be flattened
    other_extractors: dict = {}
    extra_data: dict = {}  # this will added to all the scraped items
    callback_urls: list = []
    job_id: str = lambda x: generate_uuid()

    def start_requests(self):
        if self.start_urls.__len__() > 0 and self.crawl_requests.__len__() > 0:
            raise Exception("Both start_urls and crawl_requests should not be set")
        elif self.start_urls.__len__() == 0 and self.crawl_requests.__len__() == 0:
            raise Exception("Both start_urls and crawl_requests cannot be None")
        elif self.start_urls.__len__() > 0:
            for start_url in self.start_urls:
                yield scrapy.Request(start_url, self.parse)
        else:
            for crawl_request in self.crawl_requests:
                yield scrapy.Request(crawl_request.url, self.parse, meta = crawl_request.meta)
 


    @property
    def spider_name(self):
        return slugify(self.name)

    def get_request_metadata(self, response):
        metadata = {}
        metadata['spider_meta__request'] = {
            "url": response.request.url,
            "domain": get_domain(response.request.url),
            "urn": get_urn(response.request.url),
            "spider_name": self.spider_name,
            "job_id": self.job_id,
            "meta": response.request.meta
        }
        metadata['spider_meta__response'] = {
            "scraped_at": datetime.datetime.now()
        }
        metadata['spider_meta__extra_data'] = self.extra_data
        return metadata

    @abc.abstractclassmethod
    def parse_default_extractor(self, response):
        pass

    @abc.abstractclassmethod
    def parse_other_extractors(self, response):
        pass

    def parse(self, response):
        metadata = self.get_request_metadata(response)
        data = self.parse_default_extractor(response)
        other_extractors_data = self.parse_other_extractors(response)
        if other_extractors_data:
            for k, v in other_extractors_data.items():
                data[f'other_extractors__{k}'] = v
        data.update(metadata)
        yield data

    def closed(self, reason):
        if self.callback_urls:
            for callback_url in self.callback_urls:
                self.log(f"Triggering callback {callback_url}")
                res = requests.get(callback_url)
                self.log(f"Triggered callback {callback_url}. response status_code is {res.status_code}",
                         level=logging.INFO,
                         #   extra= {"spider":self.spider_name}
                         )
