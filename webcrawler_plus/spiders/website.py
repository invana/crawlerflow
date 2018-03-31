from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import os


class WCPWebsiteSpider(CrawlSpider):
    """
    This will crawl the entire website.

    using WCP_REQUEST_HEADERS_USER_AGENT variable in os will set the user-agent.

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'website_spider'

    def _build_request(self, rule, link):
        headers = {}
        user_agent_header = os.environ.get("WCP_REQUEST_HEADERS_USER_AGENT")
        if user_agent_header:
            headers = {"User-Agent": user_agent_header}
        r = Request(url=link.url, headers=headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def parse_item(self, response):
        print(response.url)
