from .base import InvanaWebsiteSpiderBase
from invana_bot.utils.selectors import get_selector_element
from invana_bot.utils.url import get_urn, get_domain
import scrapy


class InvanaWebsiteSpider(InvanaWebsiteSpiderBase):
    """
    This will crawl the entire website.

    using WCP_REQUEST_HEADERS_USER_AGENT variable in os will set the user-agent.

    academics , faculty, department, research, fund, research proposals, funding proposals

    """
    name = 'website_spider'


class InvanaWebsiteParserSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "website_parser_spider"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.parser_config)

    def parse(self, response):
        print("response.url=========,", response.url)
        context = self.context
        parser_config = self.parser_config
        data = {}
        data['url'] = response.url
        max_pages = parser_config.get("next_page_selector", {}).get("max_pages", 1)
        current_page_count = response.meta.get('current_page_count', 1)
        for selector in self.parser_config.get('data_selectors', []):
            if selector.get('selector_attribute') == 'element' and len(selector.get('child_selectors', [])) > 0:
                # TODO - currently only support multiple elements strategy. what if multiple=False
                elements = response.css(selector.get('selector'))
                elements_data = []
                for item_no, el in enumerate(elements):
                    item_no = item_no + 1  # because enumerate starts from 0
                    datum = {}
                    for child_selector in selector.get('child_selectors', []):
                        _d = get_selector_element(el, child_selector)
                        datum[child_selector.get('id')] = _d.strip() if _d else None
                    datum['item_no'] = item_no
                    elements_data.append(datum)
                data[selector.get('id')] = elements_data
            else:
                _d = get_selector_element(response, selector)
                data[selector.get('id')] = _d.strip() if _d else None
        if context is not None:
            data.update({"context": context})
        yield data
        if current_page_count < max_pages:
            next_selector = parser_config.get('next_page_selector').get('selector')
            if next_selector:
                if parser_config.get('next_page_selector').get('selector_type') == 'css':
                    next_page = response.css(next_selector + "::attr(href)").extract_first()
                elif parser_config.get('next_page_selector').get('selector_type') == 'xpath':
                    next_page = response.xpath(next_selector + "::attr(href)").extract_first()
                else:
                    next_page = None
                current_page_count = current_page_count + 1
                if next_page:
                    if not "://" in next_page:
                        next_page_url = "https://" + get_domain(response.url) + next_page
                    else:
                        next_page_url = next_page
                    yield scrapy.Request(next_page_url, callback=self.parse,
                                         meta={"current_page_count": current_page_count}
                                         )

        else:
            print("### ended", response.url, current_page_count, max_pages)
