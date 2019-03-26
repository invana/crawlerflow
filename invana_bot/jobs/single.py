from invana_bot.runners.single import SingleCrawlerRunner
from .base import CTIJobGeneratorBase
from datetime import datetime


class SingleCrawlJobGenerator(CTIJobGeneratorBase):
    """
    InvanaBot single crawler job generator




    """

    def create_job(self,
                   current_crawler=None,
                   context=None,
                   spider_cls=None):
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()

        settings_from_manifest = current_crawler.get("settings", {})
        actual_settings = self.settings
        actual_settings['DOWNLOAD_DELAY'] = settings_from_manifest.get("download_delay", 0)
        runner = SingleCrawlerRunner(settings=actual_settings,
                                     current_crawler=current_crawler,
                                     job_id=self.job_id,
                                     context=context,
                                     spider_cls=spider_cls)
        job, errors = runner.crawl()
        return {"crawler_job": job, "crawler_job_errors": errors, "runner": runner}
