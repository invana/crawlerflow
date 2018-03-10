from scrapy import spider
from scrapy import signals
from scrapy.http import Request
from scrapy.utils.trackref import object_ref
from scrapy.utils.url import url_is_from_spider
from scrapy.utils.deprecate import create_deprecated_class
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.deprecate import method_is_overridden
import warnings
from scrapy.extensions.httpcache import FilesystemCacheStorage

class InvanaSpider(spider.Spider):
    """


    """
    download_delay = 0.1 # delay between two requests

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
