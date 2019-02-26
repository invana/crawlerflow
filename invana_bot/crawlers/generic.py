from .base import InvanaCrawlerBase
from invana_bot.pipelines.default import WebCrawlerPipeline
from datetime import datetime


class InvanaWebCrawler(InvanaCrawlerBase):
    """
    Split the bot into website crawler, feeds crawler, api crawler,

    """

    def create_jobs(self, pipeline=None, context=None):
        self.setup_crawler_type_settings(crawler_type="websites")
        if context is None:
            context = {}
        if 'job_id' not in context.keys():
            context['job_id'] = self.job_id
            context['job_started'] = datetime.now()
        pipeline = WebCrawlerPipeline(pipeline=pipeline, job_id=self.job_id, context=context)
        jobs = pipeline.run()
        self.jobs.extend(jobs)
        return jobs

    def get_settings(self):
        return self.settings

    def get_jobs(self):
        return self.jobs
