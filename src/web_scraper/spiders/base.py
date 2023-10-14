import scrapy
import datetime
import abc
from slugify import slugify
from web_scraper.utils import get_domain, get_urn, generate_uuid
import requests
import logging


class SpiderBase(scrapy.Spider):
    
    name:str = "default-spider-name"
    start_urls: list = []
    downloader: str = "default"
    spider_type: str = "APISpider"
    custom_settings: dict  = {}
    default_extractor: dict = None # this will be flattened
    other_extractors: dict = {}
    extra_data: dict = {} # this will added to all the scraped items 
    callback_urls: list = []
    job_id: str = lambda x: generate_uuid()

    @property
    def spider_name(self):
        return slugify(self.name)


    def get_request_metadata(self, response):
        metadata = {
            "meta__url": response.request.url,
            "meta__domain": get_domain(response.request.url),
            "meta__urn": get_urn(response.request.url),
            "meta__scraped_at": datetime.datetime.now(),
            "meta__scraper_name": self.spider_name,
            "meta__job_id": self.job_id
        }
        if self.extra_data:
            for k, v in self.extra_data.items():
                metadata[f"meta__{k}"] = v
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


