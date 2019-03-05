from invana_bot.utils.config import process_config


def process_pipe(parser_config=None):
    return process_config(parser_config)


def process_pipeline_config(parsers=None):
    print("parsers", parsers)
    # TODO - validate the config too
    for parser in parsers:
        for extractor in parser.get('data_extractors', []):
            extractor['data_selectors'] = process_pipe(extractor)['data_selectors']
    print("parsers", parsers)
    return parsers
