from .base import InvanaWebsiteSpiderBase
import os
from invana_bot.utils.selectors import get_selector_element


class InvanaWebsiteSpider(InvanaWebsiteSpiderBase):
    """
    This will crawl the entire website.

    using WCP_REQUEST_HEADERS_USER_AGENT variable in os will set the user-agent.

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'website_spider'

    def parse_item(self, response):
        print(response.url)


class InvanaWebsiteParserSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "invana_website_parser_spider"

    def parse_item(self, response):
        print("Parser=========,", response.url)
        data = {}
        data['url'] = response.url
        for selector in self.parser_config['data_selectors']:
            if selector.get('selector_attribute') == 'element' and \
                    len(selector.get('child_selectors', [])) > 0:
                # TODO - currently only support multiple elements strategy. what if multiple=False
                elements = response.css(selector.get('selector'))
                elements_data = []
                for el in elements:
                    datum = {}
                    for child_selector in selector.get('child_selectors', []):
                        _d = get_selector_element(el, child_selector)
                        datum[child_selector.get('id')] = _d.strip() if _d else None
                        elements_data.append(datum)
                data[selector.get('id')] = elements_data
            else:
                _d = get_selector_element(response, selector)
                data[selector.get('id')] = _d.strip() if _d else None
        yield data

        next_selector = self.parser_config.get('next_page_selector').get('selector')
        print(next_selector)
        if next_selector:
            if self.parser_config.get('next_page_selector').get('selector_type') == 'css':
                next_pages = response.css(next_selector)
            elif self.parser_config.get('next_page_selector').get('selector_type') == 'xpath':
                next_pages = response.xpath(next_selector)
            else:
                next_pages = []
            for next_page in next_pages:
                yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        print(response.url)
