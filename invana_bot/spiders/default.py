from .base import InvanaWebsiteSpiderBase
from invana_bot.utils.url import get_domain
from invana_bot.extractors.content import CustomContentExtractor, ParagraphsExtractor
import scrapy

LINK_FROM_FIELD = "link_from_field"


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
        print("========", extractor_name, data)
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
        print("get_subdocument_key", extractor_name, pipe)
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
        data = {}
        for extractor in pipe['data_extractors']:
            extracted_data = self.run_extractor(response=response, extractor=extractor, )
            data.update(extracted_data)
        if context is not None:
            data.update({"context": context})
        yield data
        for traversal in pipe.get('traversals', []):
            print("traversal", traversal)
            if traversal['traversal_type'] == "pagination":
                # TODO - move this to run_pagination_traversal(self, response=None, traversal=None) method;
                traversal_config = traversal['pagination']
                max_pages = traversal_config.get("max_pages", 1)
                current_page_count = response.meta.get('current_page_count', 1)
                print("max_pages", max_pages, current_page_count)
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
            elif traversal['traversal_type'] == LINK_FROM_FIELD:
                next_pipe_id = traversal['next_pipe_id']
                traversal_config = traversal[LINK_FROM_FIELD]

                subdocument_key = self.get_subdocument_key(pipe=pipe, extractor_name=traversal_config['extractor_name'])
                for item in data[subdocument_key]:
                    traversal_url = item[traversal[LINK_FROM_FIELD]['field_name']]

                    print("traversal_config data", next_pipe_id, traversal_url, data)
                    next_pipelet = self.get_pipe(pipe_id=next_pipe_id, pipeline=pipeline)
                    yield scrapy.Request(
                        traversal_url, callback=self.parse,
                        meta={"pipeline": pipeline,
                              "pipe": next_pipelet
                              }
                    )
