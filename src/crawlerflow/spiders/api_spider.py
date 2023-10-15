from .base import SpiderBase
import json


class APISpider(SpiderBase):
    
    def parse_default_extractor(self, response):
        return json.loads(response.body)
