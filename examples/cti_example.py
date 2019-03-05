from invana_bot.crawlers.generic import InvanaWebCrawler
import json

cti_config = json.load(open("./cti_example.json"))
context = {
    "extra_info": "2019-1-1 something",
    "author": "Ravi@Invana"
}

if __name__ == '__main__':
    crawler = InvanaWebCrawler(
        cache_database_uri="mongodb://127.0.0.1",
        storage_database_uri="mongodb://127.0.0.1",
        cache_database="mongodb",
        storage_database="mongodb",
    )

    print("cti_config", cti_config['crawlers'])
    job = crawler.create_job(
        cti_config=cti_config,
        context=context
    )
    print("all_jobs", job)
    crawler.start_jobs(jobs=[job])
