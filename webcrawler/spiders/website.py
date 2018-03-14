from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class InvanaWebsiteSpider(CrawlSpider):
    """

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'website_spider'

    # rules = (
    #     Rule(LinkExtractor(deny=(r'event-created/', r'event', r'content', r'career',
    #                              r'about', r'convocation', r'gallery')), callback='parse_item', follow=True, ),
    # )
    #
    # def parse_item(self, response):
    #     print(response.url)
