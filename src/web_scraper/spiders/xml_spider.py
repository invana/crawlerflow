from scrapy.spiders import XMLFeedSpider as _XMLFeedSpider
import feedparser
from .base import SpiderBase


class XMLFeedSpider(SpiderBase):
    
    
    def parse_default_extractor(self, response):
        return feedparser.parse(response.body)
 