from invana_bot.utils.config import InvanaBotConfigValidator

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
validator = InvanaBotConfigValidator(config=cti_manifest)
validator.validate()
