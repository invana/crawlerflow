DEFAULT_SETTINGS_BASE = {
    'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
    'HTTPCACHE_ENABLED': True,
    'TELNETCONSOLE_PORT': [6023, 6073],
    'ITEM_PIPELINES': {
        'invana_bot.core.storages.default.InvanaDataPipeline': 1,
    },
    'DOWNLOADER_MIDDLEWARES': {
        "invana_bot.core.downloaders.spider_analytics.IndividualSpiderRequestStats": 121,
        "invana_bot.core.downloaders.spider_analytics.IndividualSpiderResponseStats": 999,
    }
}
DEFAULT_SETTINGS = {}
DEFAULT_SETTINGS.update(DEFAULT_SETTINGS_BASE)
