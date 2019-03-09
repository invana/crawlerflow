from invana_bot.utils.config import validate_cti_config
from invana_bot.crawlers.generic import InvanaBotWebCrawler
from invana_bot.settings import DEFAULT_SETTINGS
import json

cti_manifest = json.load(open("../eti_full.json"))


def transformation_fn(results):
    results_cleaned = []
    for result in results:
        for blog in result.get("blogs", []):
            results_cleaned.append(blog)

    return results_cleaned


cti_manifest['transformations'] = [
    {
        "transformation_id": "default",
        "transformation_fn": transformation_fn
    }
]
context = {
    "author": "https://github.com/rrmerugu",
    "description": "Crawler that scrapes invanalabs xyz"
}
errors = validate_cti_config(cti_manifest)
if len(errors) > 0:
    print("Please fix manifest errors")

crawler = InvanaBotWebCrawler(
    settings=DEFAULT_SETTINGS
)

print("cti_manifest", cti_manifest['crawlers'])
job = crawler.create_job(
    cti_manifest=cti_manifest,
    context=context
)
print("job", job)
crawler.start_job(job=job)
