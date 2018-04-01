from webcrawler_plus.settings import EXTRACTED_DATA_COLLECTION, DATA_COLLECTION
from webcrawler_plus.parser import crawl_websites


# class WebCrawlerPlusBase(object):
#     """
#     The webcrawler plus runner.
#
#     """
#
#     base_settings = {
#         'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
#         'HTTPCACHE_ENABLED': True,
#     }
#
#     def __init__(self,
#                  settings=None,
#                  urls=[]
#                  ):
#         """
#
#
#         cache_enabled is needed to control the cache expiring etc, but we always want to save the data!(may be not necessary)
#
#
#
#         cache_db_credentials = storage_db_credentials= {
#             "host" : "127.0.0.1",
#             "port": "27017",
#             "username": "admin",
#             "password": "password",
#             "cache_collection": "cache_collection"
#             "storage_collection": "extracted_data_collection"
#             "database": "some_database"
#         }
#
#         :param cache_db_credentials:
#         :param cache_db:
#         :param cache_enabled:
#         :param storage_db_credentials:
#         :param storage_db:
#         :param urls:
#         """
#         if type(urls) is None:
#             raise Exception("urls should be list type.")
#         if len(urls) is 0:
#             raise Exception("urls length should be atleast one.")
#
#         if settings is None:
#             self.settings = self.settings
#
#     def run(self, ):
#         raise Exception("Not implemented")


class WebCrawlerPlus(object):
    """


    database_credentials = {
            "host" : "127.0.0.1",
            "port": "27017",
            "username": "admin",
            "password": "password",
            "cache_collection": "cache_collection"
            "storage_collection": "extracted_data_collection"
            "database": "some_database"
        }

    """
    settings = {
        'COMPRESSION_ENABLED': False,  # this will save the data in normal text form, otherwise to bytes form.
        'HTTPCACHE_ENABLED': True,
    }

    def __init__(self,
                 database=None,
                 database_credentials=None,
                 http_cache_enabled=True,
                 log_level="INFO",
                 extra_settings=None,

                 **kwargs):

        self.settings['HTTPCACHE_ENABLED'] = http_cache_enabled
        self.settings['WCP_CRAWLER_COLLECTION'] = database_credentials.get('cache_collection', DATA_COLLECTION)
        self.settings['WCP_CRAWLER_EXTRACTION_COLLECTION'] = database_credentials.get('storage_collection',
                                                                                      EXTRACTED_DATA_COLLECTION)

        if database == "mongodb":
            self.settings['HTTPCACHE_MONGODB_DATABASE'] = database_credentials.get('database', 'webcrawler_plus')
            self.settings['HTTPCACHE_HOST'] = database_credentials.get('host', '127.0.0.1')
            self.settings['HTTPCACHE_MONGODB_PORT'] = database_credentials.get('port', '8983')
            self.settings['HTTPCACHE_MONGODB_USERNAME'] = database_credentials.get('username', '')
            self.settings['HTTPCACHE_MONGODB_PASSWORD'] = database_credentials.get('password', '')

            self.settings['ITEM_PIPELINES'] = {'webcrawler_plus.pipelines.mongodb.MongoDBPipeline': 1}
            self.settings['HTTPCACHE_STORAGE'] = "webcrawler_plus.httpcache.mongodb.MongoDBCacheStorage"
        elif database == "elasticsearch":
            self.settings['HTTPCACHE_ES_DATABASE'] = database_credentials.get('database', 'webcrawler_plus')
            self.settings['HTTPCACHE_HOST'] = database_credentials.get('host', '127.0.0.1')

            self.settings['ITEM_PIPELINES'] = {'webcrawler_plus.pipelines.elasticsearch.ElasticsearchPipeline': 1}
            self.settings['HTTPCACHE_STORAGE'] = "webcrawler_plus.httpcache.elasticsearch.ESCacheStorage"

            # settings['HTTPCACHE_ES_PORT'] = database_credentials.get('port', '9200') # TODO - implement
        elif database == "solr":
            self.settings['HTTPCACHE_ES_DATABASE'] = database_credentials.get('database', 'webcrawler_plus')
            self.settings['HTTPCACHE_HOST'] = database_credentials.get('host', '127.0.0.1')
            self.settings['HTTPCACHE_SOLR_PORT'] = database_credentials.get('port', '8993')
            self.settings['ITEM_PIPELINES'] = {'webcrawler_plus.pipelines.solr.SolrPipeline': 1}
            self.settings['HTTPCACHE_STORAGE'] = "webcrawler_plus.httpcache.solr.SolrCacheStorage"
        else:
            raise Exception("We only support, elasticsearch, solr and mongodb at this moment.")

        self.settings['LOG_LEVEL'] = log_level
        if extra_settings:
            self.settings.update(extra_settings)  # over riding or adding extra settings

    def run(self,
            urls=None,
            ignore_urls_with_words=None,
            allow_only_with_words=None,
            follow=True):

        if type(urls) is None:
            raise Exception("urls should be list type.")
        if len(urls) is 0:
            raise Exception("urls length should be atleast one.")

        crawl_websites(urls=urls,
                       settings=self.settings,
                       ignore_urls_with_words=ignore_urls_with_words,
                       allow_only_with_words=allow_only_with_words,
                       follow=follow
                       )
