from invana_bot.spiders.web import InvanaBotSingleWebCrawler
from scrapy.spiders import Rule
from invana_bot.utils.config import validate_spider_config
from scrapy.linkextractors import LinkExtractor
from .base import RunnerEngineBase


class InvanaBotSingleCrawlerRunnerEngine(RunnerEngineBase):
    """

    InvanaBotSingleCrawlerRunnerEngine


      spider_id: blog_list
      allowed_domains:
        - "blog.scrapinghub.com"
      extractors:
      - extractor_type: ParagraphsExtractor
        extractor_id: paragraphs
        data_storage:
          include_url: true
          collection_name: paragraphs
      - extractor_type: MetaTagExtractor
        extractor_id: meta_tag
        data_storage:
          include_url: true
      settings:
        data_storages:
        - storage_id: default
          storage_type: mongodb
          connection_uri: mongodb://127.0.0.1/spiders_data_index
          collection_name: blog_list
        bot_name: InvanaBot


    """

    def __init__(self,
                 job_id=None,
                 spider_config=None,
                 manifest=None,
                 spider_cls=None,
                 context=None,
                 # manifest_validator=None,
                 **kwargs
                 ):
        """ansf

        :param spider_config: single spider data
        :param manifest: over all manifest data, including spiders, transformations
        :param job_id: this is used for transformating the data of a single job(job_id).
        :param spider_cls:
        :param context: extra data that you may want to access in parse() of spider.
        :param extra_arguments: extra data that you may want to access in parse() of spider.
        # :param manifest_validator: Validator for spider_cls
        """

        self.spider_config = spider_config
        self.manifest = manifest
        self.job_id = job_id
        self.spider_cls = spider_cls
        self.context = context or {}
        self.extra_arguments = context or {}
        # self.manifest_validator = manifest_validator

    def crawl(self):
        errors = validate_spider_config(self.manifest)
        if len(errors) == 0:
            cti_job = self.run()
            return cti_job, errors
        else:
            return None, errors

    def validate_pipe(self):
        must_have_keys = ["spider_id", "extractors"]
        optional_keys = ["traversals"]
        for key in must_have_keys:
            if key not in self.manifest.keys():
                raise Exception(
                    "invalid parser data, should have the following keys; {}".format(",".join(must_have_keys)))

    def validate_traversal(self):
        pass  # TODO - implement this

    def validate_extractor(self):
        pass  # TODO - implement this

    def get_traversals(self):
        return self.manifest.get("traversals", [])

    def get_extractors(self):
        return self.manifest.get("extractors", [])

    def generate_spider_kwargs(self):
        extractor = LinkExtractor()
        rules = [
            Rule(extractor, follow=True)  # TODO - add regex types of needed.
        ]
        print(self.manifest)
        spider_kwargs = {
            "start_urls": self.spider_config['start_urls'],
            "allowed_domains": [],
            "rules": rules,
            "spider_config": self.spider_config,
            "manifest": self.manifest,
            "context": self.context,
            # "default_storage":
        }
        spider_kwargs.update(self.extra_arguments)
        return spider_kwargs

    def run(self):
        spider_cls = self.spider_cls or InvanaBotSingleWebCrawler
        spider_kwargs = self.generate_spider_kwargs()
        return {"spider_cls": spider_cls, "spider_kwargs": spider_kwargs}
