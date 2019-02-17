from invana_bot.utils.config import validate_config, process_config


def process_pipe(parser_config=None):
    return process_config(parser_config)


def process_pipeline_config(pipeline=None):
    # TODO - validate the config too
    for pipe in pipeline['pipeline']:
        for extractor in pipe.get('data_extractors', []):
            extractor['data_selectors'] = process_pipe(extractor)['data_selectors']

    return pipeline
