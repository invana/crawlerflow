from scrapy.spiders import CrawlSpider
from scrapy.http import Request

import os


class WebCrawlerBase(CrawlSpider):

    def _build_request(self, rule, link):
        headers = {}
        user_agent_header = os.environ.get("WCP_REQUEST_HEADERS_USER_AGENT")
        if user_agent_header:
            headers = {"User-Agent": user_agent_header}
        r = Request(url=link.url, headers=headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r
