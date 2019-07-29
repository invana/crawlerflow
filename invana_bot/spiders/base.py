from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from invana_bot.utils.spiders import get_spider_from_list
import os
from invana_bot.traversals.generic import GenericLinkExtractor
import scrapy


class WebCrawlerBase(CrawlSpider):
    """

    TODO - document why we need this as base method.

    """

    spider_id = None
    spider_config = None
    spider_data_storage = None
    manifest = {}

    def post_parse(self, response=None):
        pass

    def parse_error(self, failure):
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.parse_error,
                dont_filter=True,
                meta={
                    "current_request_traversal_page_count": 0,
                    "spider_config": self.spider_config,
                    "manifest": self.manifest
                }
            )

    def get_spider_config(self, response=None):
        if response.meta.get("spider_config"):
            return response.meta.get("spider_config")
        else:
            return self.spider_config

    @staticmethod
    def get_default_storage(settings=None, spider_config=None):
        data_storages = settings.get("DATA_STORAGES", [])
        default_storage = None
        spider_storage_id = "default"
        for data_storage in data_storages:
            __storage_id = data_storage.get("storage_id") or data_storage.get("STORAGE_ID")
            if __storage_id == spider_storage_id:
                return data_storage
        return default_storage

    @staticmethod
    def prepare_data_for_yield(data=None, collection_name=None, storage_id="default"):
        return {
            "_data_storage_id": storage_id,
            "_data_storage_collection_name": collection_name,
            "_data": data
        }

    def _build_request(self, rule, link):
        headers = {}
        user_agent_header = os.environ.get("WCP_REQUEST_HEADERS_USER_AGENT")
        if user_agent_header:
            headers = {"User-Agent": user_agent_header}
        r = Request(url=link.url, headers=headers, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    @staticmethod
    def is_this_request_from_same_traversal(response, traversal):
        """
        This mean the current request came from this  traversal,
        so we can put max pages condition on this, otherwise for different
        traversals of different spiders, adding max_page doest make sense.
        """
        traversal_id = traversal['traversal_id']
        current_request_traversal_id = response.meta.get('current_request_traversal_id', None)
        return current_request_traversal_id == traversal_id

    def make_traversal_requests(self, to_traverse_links_list=None):
        traversal_requests = []
        for to_traverse_link in to_traverse_links_list:
            traversal_requests.append(scrapy.Request(
                to_traverse_link.get("link"),
                callback=self.parse,
                errback=self.parse_error,
                meta=to_traverse_link.get("meta", {})
            ))
        return traversal_requests

    @staticmethod
    def run_traversal(response=None, traversal=None, **kwargs):

        selector_type = traversal.get("selector_type", "css")
        kwargs = {}
        if selector_type == "css":
            kwargs['restrict_css'] = (traversal.get("selector_value"),)
        elif selector_type == "xpath":
            kwargs['restrict_xpaths'] = (traversal.get("selector_value"),)

        if traversal.get("allow_domains", []) == ["*"]:
            kwargs['allow_domains'] = ()
        else:
            kwargs['allow_domains'] = traversal.get("allow_domains", [])
        return GenericLinkExtractor(**kwargs).extract_links(response=response)

    def run_traversals(self, spider_config=None, response=None):
        """
        if spider_traversal_id is None, it means this response originated from the
        request raised by the start urls.

        If it is Not None, the request/response is raised some traversal strategy.
        """
        current_request_traversal_id = response.meta.get('current_request_traversal_id', None)
        current_request_traversal_page_count = response.meta.get('current_request_traversal_page_count', 0)

        """
        Note on current_request_spider_id:
        This can never be none, including the ones that are started by start_urls .
        """
        traversal_data = {}
        to_traverse_links_list = []
        spider_traversals = spider_config.get('traversals', [])
        spiders = response.meta.get("manifest", {}).get("spiders")

        for traversal in spider_traversals:
            next_spider_id = traversal['next_spider_id']
            next_spider = get_spider_from_list(spider_id=next_spider_id, spiders=spiders)

            traversal['allow_domains'] = next_spider.get("allowed_domains", [])
            traversal_id = traversal['traversal_id']
            traversal_max_pages = traversal.get('max_pages', 1)

            traversal_links = []
            is_this_request_from_same_traversal = self.is_this_request_from_same_traversal(response, traversal)
            # print("is_this_request_from_same_traversal", is_this_request_from_same_traversal)
            # print("current_request_traversal_page_count", current_request_traversal_page_count)
            # print("traversal_max_pages", traversal_max_pages)
            # print(" current_request_traversal_page_count < traversal_max_pages",
            # current_request_traversal_page_count < traversal_max_pages)
            shall_traverse = False

            if current_request_traversal_id is None:
                """
                start urls will not have this traversal_id set, so we should allow then to traverse
                """
                shall_traverse = True

            elif is_this_request_from_same_traversal and current_request_traversal_page_count < traversal_max_pages:
                """
                This block will be valid for the traversals from same spider_id, ie., pagination of a spider 
                """

                shall_traverse = True

            elif is_this_request_from_same_traversal:
                """
                """
                shall_traverse = True

            elif is_this_request_from_same_traversal is False and current_request_traversal_page_count < traversal_max_pages:
                """
                This for the spider_a traversing to spider_b, this is not pagination, but trsversing between 
                spiders.
                """
                shall_traverse = True
            # print("shall_traverse: {}".format(traversal_id), shall_traverse)
            if shall_traverse:
                traversal_links = self.run_traversal(response=response, traversal=traversal)
                traversal_data[traversal_id] = {"traversal_urls": traversal_links}
                """
                Then validate for max_pages logic if traversal_id's traversal has any!.
                This is where the further traversal for this traversal_id  is decided 
                """
                max_pages = traversal.get("max_pages", 1)
                for link in traversal_links:

                    """
                    we are already incrementing, the last number, so using <= might make it 6 pages when 
                    max_pages is 5 
                    """
                    if current_request_traversal_page_count < max_pages:
                        # print("=======current_request_traversal_page_count", current_request_traversal_page_count)
                        # print("link", link)
                        # print("-----------------------------------")

                        # print("===>>>>meta", meta)
                        to_traverse_links_list.append(
                            {
                                "link": link,
                                "meta": {
                                    "spider_config": next_spider,
                                    "manifest": response.meta.get("manifest"),
                                    "current_request_traversal_id": traversal_id,
                                    "current_request_traversal_page_count": current_request_traversal_page_count,

                                }}
                        )

                    current_request_traversal_page_count += 1

            print("=================================================")
            print("{} traversal_links for traversal:".format(len(traversal_links), traversal_id))
            print("=================================================")
        return traversal_data, to_traverse_links_list
