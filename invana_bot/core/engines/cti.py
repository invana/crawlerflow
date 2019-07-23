from invana_bot.utils.spiders import get_spider_from_list
from invana_bot.utils.config import validate_cti_config
from .base import RunnerEngineBase
from .single import InvanaBotSingleCrawlerRunnerEngine


class InvanaBotRunnerEngine(RunnerEngineBase):
    """

    InvanaBotRunnerEngine


    """

    def __init__(self, job_id=None, spider_cls=None, manifest=None):
        self.job_id = job_id
        self.spider_cls = spider_cls
        self.manifest = manifest

    def crawl(self):
        errors = validate_cti_config(self.manifest)
        if len(errors) == 0:

            initial_spider_config = get_spider_from_list(
                spider_id=self.manifest['init_spider']['spider_id'],
                spiders=self.manifest['spiders']
            )
            initial_spider_config['start_urls'] = self.manifest['init_spider']['start_urls']
            spider_runner = InvanaBotSingleCrawlerRunnerEngine(
                job_id=self.job_id,
                spider_cls=self.spider_cls,
                spider_config=initial_spider_config,
                manifest=self.manifest,
            )
            job = spider_runner.run()

            return job, errors
        else:
            return None, errors
