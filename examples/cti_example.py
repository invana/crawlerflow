from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
import json

cti_config = json.load(open("./cti_example_list_and_detail_traversals.json"))
context = {
    "extra_info": "2019-1-1 something",
    "author": "Ravi@Invana"
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
