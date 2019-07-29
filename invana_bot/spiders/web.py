from .base import WebCrawlerBase
from importlib import import_module
from invana_bot.utils.url import get_domain
import scrapy


class InvanaBotSingleWebCrawler(WebCrawlerBase):
    """
    This is generic spider
    """
    name = "InvanaBotSingleWebCrawler"

    def closed(self, reason):
        print("spider closed with payload:", reason, self.spider_config.get('cti_id'))

    @staticmethod
    def run_extractor(response=None, extractor=None):
        extractor_type = extractor.get("extractor_type")
        extractor_id = extractor.get("extractor_id")
        print("Running extractor {} on url {}".format(extractor_id, response.url))
        driver_klass_module = import_module(f'invana_bot.extractors')
        driver_klass = getattr(driver_klass_module, extractor_type)

        if extractor_type is None:
            return {extractor_id: None}
        else:
            try:
                extractor_object = driver_klass(response=response,
                                                extractor=extractor,
                                                extractor_id=extractor_id)
                data = extractor_object.run()
                return data
            except Exception as e:
                print("Failed to run the extractor_id {} on url {} with error:".format(extractor_id,
                                                                                       response.url,
                                                                                       e))
        return {extractor_id: None}

    def parse(self, response=None):
        self.logger.info("======Parsing the url: {}".format(response.url))
        spider_config = self.get_spider_config(response=response)
        """
        Use this when multiple databases concept is implemented

        default_storage = self.get_default_storage(
            settings=self.settings,
            spider_config=spider_config
        )
        """
        data = {}
        for extractor in spider_config.get('extractors', []):
            extracted_data = self.run_extractor(response=response, extractor=extractor)
            data.update(extracted_data)

        context = self.manifest.get("context")
        if context is not None:
            data.update({"context": context})
        data['url'] = response.url
        data['screenshot'] = response.meta.get("screenshot")
        data['domain'] = get_domain(response.url)
        data['context']['spider_id'] = spider_config['spider_id']
        traversal_data, to_traverse_links_list = self.run_traversals(spider_config=spider_config, response=response)
        data.update(traversal_data)
        # This will save the data
        yield self.prepare_data_for_yield(
            data=data,
            # storage_id=default_storage.get("storage_id"),
            # collection_name=default_storage.get("collection_name")
        )

        # This will initiate new traversals
        traversal_requests = self.make_traversal_requests(to_traverse_links_list=to_traverse_links_list)
        for traversal_request in traversal_requests:
            yield traversal_request
        self.post_parse(response=response)
