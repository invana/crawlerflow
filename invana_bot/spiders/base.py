from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output

import os


class InvanaWebsiteSpiderBase(CrawlSpider):

    def _build_request(self, rule, link):
        headers = {}
        user_agent_header = os.environ.get("WCP_REQUEST_HEADERS_USER_AGENT")
        if user_agent_header:
            headers = {"User-Agent": user_agent_header}
        r = Request(url=link.url, headers=headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if self.parser_config:
            crawler_metadata = self.parser_config.get("crawler_metadata", None)
            print("=============crawler_metadata", crawler_metadata)

        else:
            crawler_metadata = None
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                if crawler_metadata is not None:
                    requests_or_item.update({"crawler_metadata": crawler_metadata})
                yield requests_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                if crawler_metadata is not None:
                    request_or_item.update({"crawler_metadata": crawler_metadata})
                yield request_or_item
