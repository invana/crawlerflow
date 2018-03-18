import scrapy
from webcrawler.webcrawler.utils.selectors import get_selector_element


class SearchEngineBaseSpider(scrapy.Spider):
    """
    bing search engine
    """
    name = 'search_engine_base'

    def parse(self, response):
        data = {}
        data['url'] = response.url
        for selector in self.config['data_selectors']:
            if selector.get('selector_attribute') == 'element' and \
                    len(selector.get('child_selectors', [])) > 0:
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

        next_selector = self.config.get('next_page_selector').get('selector')
        if next_selector:
            if self.config.get('next_page_selector').get('selector_type') == 'css':
                next_pages = response.css(next_selector)
            elif self.config.get('next_page_selector').get('selector_type') == 'xpath':
                next_pages = response.xpath(next_selector)
            else:
                next_pages = []
            for next_page in next_pages:
                yield response.follow(next_page, self.parse)
