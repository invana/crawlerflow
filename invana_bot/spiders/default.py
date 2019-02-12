from .base import InvanaWebsiteSpiderBase
from invana_bot.utils.selectors import get_selector_element
from invana_bot.utils.url import get_domain
import scrapy


class DefaultInvanaPipeSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "DefaultInvanaPipeSpider"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.pipe)

    def run_extractor(self, response=None, extractor=None):
        context = self.context
        data = {}
        data['url'] = response.url
        for selector in extractor.get('data_selectors', []):
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
        return data

    def parse(self, response=None):
        pipe = self.pipe
        for extractor in pipe['data_extractors']:
            data = self.run_extractor(response=response, extractor=extractor, )
            yield data

        for traversal in pipe['traversals']:
            print("traversal", traversal)
            if traversal['traversal_type'] == "pagination":
                # TODO - move this to run_pagination_traversal(self, response=None, traversal=None) method;
                pagination = traversal['pagination']
                max_pages = pagination.get("max_pages", 1)
                current_page_count = response.meta.get('current_page_count', 1)
                print("max_pages", max_pages, current_page_count)
                if current_page_count < max_pages:
                    next_selector = pagination.get('selector')
                    if next_selector:
                        if pagination.get('selector_type') == 'css':
                            next_page = response.css(next_selector + "::attr(href)").extract_first()
                        elif pagination.get('selector_type') == 'xpath':
                            next_page = response.xpath(next_selector + "::attr(href)").extract_first()
                        else:
                            next_page = None
                        current_page_count = current_page_count + 1
                        if next_page:
                            if not "://" in next_page:
                                next_page_url = "https://" + get_domain(response.url) + next_page
                            else:
                                next_page_url = next_page
                            # TODO - add logics to change the extractors or call a different pipe from here.
                            yield scrapy.Request(
                                next_page_url, callback=self.parse,
                                meta={"current_page_count": current_page_count}
                            )
            elif traversal['traversal_type'] == "something_else":
                pass
