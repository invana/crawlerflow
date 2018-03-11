from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class InvanaWebsiteSpider(CrawlSpider):
    name = 'srmuniv.ac.in'
    allowed_domains = ['www.srmuniv.ac.in']
    start_urls = ['http://www.srmuniv.ac.in/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
