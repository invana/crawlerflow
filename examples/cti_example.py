from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
import json

# cti_config = json.load(open("./cti_example_list_and_detail_traversals.json"))
# cti_config = json.load(open("./cti_example_same_domain_traversal.json"))
cti_config = json.load(open("./basic_example.json"))
context = {
    "job_id": "123",
    "author": "https://github.com/rrmerugu",
    "description": "Crawler that scrapes invanalabs xyz"
}

if __name__ == '__main__':
    crawler = InvanaBotWebCrawler(
        settings=DEFAULT_SETTINGS
    )

    print("cti_config", cti_config['crawlers'])
    job = crawler.create_job(
        cti_config=cti_config,
        context=context
    )
    print("all_jobs", job)
    crawler.start_jobs(jobs=[job])
