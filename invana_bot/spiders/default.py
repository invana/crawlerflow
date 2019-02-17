from .base import InvanaWebsiteSpiderBase
from invana_bot.extractors.content import CustomContentExtractor, ParagraphsExtractor
import scrapy
from invana_bot.utils.url import get_domain, get_absolute_url

TRAVERSAL_LINK_FROM_FIELD = "link_from_field"
TRAVERSAL_SAME_DOMAIN_FIELD = "same_domain"


class DefaultPipeletSpider(InvanaWebsiteSpiderBase):
    """
    This is generic spider
    """
    name = "DefaultPipeletSpider"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.pipe)

    def run_extractor(self, response=None, extractor=None):
        extractor_name = extractor.get("extractor_name")
        if extractor_name in [None, "CustomContentExtractor"]:
            extractor_object = CustomContentExtractor(response=response, extractor=extractor)
        elif extractor_name == "ParagraphsExtractor":
            extractor_object = ParagraphsExtractor(response=response, extractor=extractor)
        else:
            return
        data = extractor_object.run()
        return data

    def get_pipe(self, pipeline=None, pipe_id=None):
        pipeline = pipeline['pipeline']
        for pipe in pipeline:
            if pipe.get("pipe_id") == pipe_id:
                return pipe
        return

    def get_subdocument_key(self, pipe=None, extractor_name=None):
        """
        element is the subdocument key name.

        :param pipe:
        :return:
        """
        for extractor in pipe['data_extractors']:
            if extractor.get("extractor_name") == extractor_name:
                for selector in extractor.get('data_selectors', []):
                    if selector.get('selector_attribute') == 'element':
                        return selector.get("id")
        return

    def parse(self, response=None):

        pipe = response.meta.get("pipe")
        pipeline = response.meta.get("pipeline")
        context = self.context

        if None in [pipeline, pipe]:
            pipe = self.pipe
            pipeline = self.pipeline

        if None not in [pipe, pipeline]:
            data = {}
            for extractor in pipe['data_extractors']:
                extracted_data = self.run_extractor(response=response, extractor=extractor, )
                data.update(extracted_data)
            if context is not None:
                data.update({"context": context})
            data['url'] = response.url
            data['domain'] = get_domain(response.url)
            yield data
            for traversal in pipe.get('traversals', []):
                if traversal['traversal_type'] == "pagination":
                    # TODO - move this to run_pagination_traversal(self, response=None, traversal=None) method;
                    traversal_config = traversal['pagination']
                    max_pages = traversal_config.get("max_pages", 1)
                    current_page_count = response.meta.get('current_page_count', 1)
                    if current_page_count < max_pages:
                        next_selector = traversal_config.get('selector')
                        if next_selector:
                            if traversal_config.get('selector_type') == 'css':
                                next_page = response.css(next_selector + "::attr(href)").extract_first()
                            elif traversal_config.get('selector_type') == 'xpath':
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
                elif traversal['traversal_type'] == TRAVERSAL_LINK_FROM_FIELD:
                    next_pipe_id = traversal['next_pipe_id']
                    traversal_config = traversal[TRAVERSAL_LINK_FROM_FIELD]

                    subdocument_key = self.get_subdocument_key(pipe=pipe,
                                                               extractor_name=traversal_config['extractor_name'])
                    for item in data[subdocument_key]:
                        traversal_url = item[traversal[TRAVERSAL_LINK_FROM_FIELD]['field_name']]
                        next_pipelet = self.get_pipe(pipe_id=next_pipe_id, pipeline=pipeline)
                        yield scrapy.Request(
                            traversal_url, callback=self.parse,
                            meta={"pipeline": pipeline,
                                  "pipe": next_pipelet
                                  }
                        )
                elif traversal['traversal_type'] == TRAVERSAL_SAME_DOMAIN_FIELD:
                    all_urls = response.css("a::attr(href)").extract()
                    filtered_urls = []
                    current_domain = get_domain(response.url)
                    for url in all_urls:
                        url = get_absolute_url(url=url, origin_url=response.url)
                        if get_domain(url) == current_domain:
                            filtered_urls.append(url)

                    # max_pages = traversal.get("max_pages", 100)
                    #  implementing max_pages is difficult cos it keeps adding
                    # new 100 pages in each thread.
                    current_page_count = response.meta.get('current_page_count', 1)
                    for url in filtered_urls:
                        current_page_count = current_page_count + 1

                        yield scrapy.Request(
                            url, callback=self.parse,
                            meta={"current_page_count": current_page_count}
                        )
