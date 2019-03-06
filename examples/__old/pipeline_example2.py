from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.schedulers.generic import InvanaJobScheduler
from invana_bot.pipelines.process import process_pipeline_config

pipeline_data = {
    "pipeline_id": "free_proxy_list",
    "start_urls": ["https://free-proxy-list.net/"],
    "pipeline": [
        {  # single pipe
            "pipe_id": "blog-list",
            "data_extractors": [
                {
                    "extractor_name": "TableContentExtractor"
                },
            ],
        }
    ]
}

context = {
    "extra_info": "2019-1-1 something",
    "author": "Ravi@Invana",

}

if __name__ == '__main__':
    crawler = InvanaBotWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    pipeline_data = process_pipeline_config(pipeline=pipeline_data)

    all_job = crawler.create_job(
        pipeline=pipeline_data,
        context=context
    )

    scheduler = InvanaJobScheduler(settings=crawler.get_settings())
    scheduler.start_jobs(jobs=[all_job])
