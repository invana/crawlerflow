from invana_bot.spiders.default import InvanaBotSingleSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from invana_bot.utils.config import validate_crawler_config


class SingleCrawlerRunner(object):
    """

    crawler = {  # single pipe

        "crawler_id": "blog-list",
        "parsers": [
            {
                "data_selectors": [
                    {
                        "id": "items",
                        "selector": ".post-listing .post-item",
                        "selector_attribute": "element",
                        "multiple": True
                    }
                ],
            }
        ],
        "traversals": [{
            "traversal_type": "pagination",
            "pagination": {
                "selector": ".next-posts-link",
                "selector_type": "css",
                "max_pages": 2
            },
        }],
        "context":{
        },
        "settings": {
        }

    }

    """

    def __init__(self,
                 current_crawler=None,
                 start_urls=None,
                 job_id=None,
                 crawlers=None,
                 context=None,
                 spider_cls=None,
                 settings=None
                 ):
        """

        :param current_crawler: single crawler in the CTI flow
        :param crawlers: all the crawlers in the CTI flow
        :param context: any extra information user want to send to the crawled data or carry forward.
        :param settings:  settings to run the crawling job. .
        """
        self.current_crawler = current_crawler
        self.job_id = job_id
        self.crawlers = crawlers
        self.start_urls = start_urls
        self.settings = settings
        self.spider_cls = spider_cls
        if context:
            self.context = context
        self.validate_pipe()

    def crawl(self):
        errors = validate_crawler_config(self.current_crawler)
        if len(errors) == 0:

            parser_crawler = SingleCrawlerRunner(
                job_id=self.job_id,
                start_urls=self.current_crawler['start_urls'],
                current_crawler=self.current_crawler,
                crawlers=self.crawlers,
                context=self.context,
                spider_cls=self.spider_cls,
                settings=self.settings
            )
            cti_job = parser_crawler.run()

            return cti_job, errors
        else:
            return None, errors

    def validate_pipe(self):
        must_have_keys = ["crawler_id", "parsers"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.current_crawler.keys():
                raise Exception(
                    "invalid parser data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.current_crawler.get("traversals", [])

    def get_extractors(self):
        return self.current_crawler.get("parsers", [])

    def generate_crawler_kwargs(self):
        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]
        allowed_domains = self.current_crawler.get("settings", {}).get('allowed_domains', [])

        spider_kwargs = {
            "start_urls": self.start_urls,
            "allowed_domains": allowed_domains,
            "rules": rules,
            "current_crawler": self.current_crawler,
            "crawlers": self.crawlers,
            "context": self.context
        }
        return spider_kwargs

    def run(self):
        spider_cls = self.spider_cls or InvanaBotSingleSpider

        spider_kwargs = self.generate_crawler_kwargs()
        return {"spider_cls": spider_cls, "spider_kwargs": spider_kwargs, "spider_settings": self.settings}

    def transform_and_index(self, callback=None):
        """
        This function will handle both tranform and index

        :param callback:
        :return:
        """
        print("TODO - IMPLEMENT THIS ")
        if callback is not None:
            callback()
