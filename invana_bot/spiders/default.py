from .base import InvanaWebsiteSpiderBase
from invana_bot.utils.url import get_domain
from invana_bot.extractors.content import CustomContentExtractor
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
        extractor_object = CustomContentExtractor(response=response, extractor=extractor)
        data = extractor_object.run()
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
