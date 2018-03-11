from scrapy import spider
from scrapy.http import Request


class InvanaSpider(spider.Spider):
    """


    """

    # download_delay = 0.1  # delay between two requests

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
