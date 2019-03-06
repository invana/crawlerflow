from invana_bot.utils.config import process_config


def process_pipe(parser_config=None):
    return process_config(parser_config)


def process_pipeline_config(crawlers=None):
    print("crawlers", crawlers)
    # TODO - validate the config too
    for crawler in crawlers:
        for extractor in crawler.get('parsers', []):
            extractor['data_selectors'] = process_pipe(extractor)['data_selectors']
    print("crawlers", crawlers)
    return crawlers
