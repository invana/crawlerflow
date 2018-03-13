from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class InvanaWebsiteSpider(CrawlSpider):
    """

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'srmuniv.ac.in'
    allowed_domains = ['www.srmuniv.ac.in']
    start_urls = ['http://www.srmuniv.ac.in/']

    rules = (
        Rule(LinkExtractor(deny=(r'event-created/', r'event', r'content',r'career',
                                 r'about', r'convocation', r'gallery')), callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        print(response.url)
