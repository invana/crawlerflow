from .base import SpiderBase
import importlib


class HTMLSpider(SpiderBase):
    """
  
    """
 

    def parse_default_extractor(self, response):
          spider_cls = getattr(importlib.import_module(f"web_scraper.extractors"), self.default_extractor['extractor_type'])
          extractor = spider_cls(response, self.default_extractor['fields'] )
          return extractor.extract()
    
    def parse_other_extractors(self, response):
        data = {}
        for extractor_id, single_extractor_config in self.other_extractors.items():
            spider_cls = getattr(importlib.import_module(f"web_scraper.extractors"), single_extractor_config['extractor_type'])
            extractor = spider_cls(response, single_extractor_config['fields'] )
            data[extractor_id] = extractor.extract()
        return data

