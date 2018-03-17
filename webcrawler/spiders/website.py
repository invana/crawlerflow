from scrapy.spiders import CrawlSpider


class InvanaWebsiteSpider(CrawlSpider):
    """
    This will crawl the entire website

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'website_spider'

    def parse_item(self, response):
        print(response.url)
