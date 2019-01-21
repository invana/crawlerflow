from invana_bot.settings import EXTRACTED_DATA_COLLECTION, CACHE_COLLECTION
from invana_bot.parser import crawl_websites

# class InvanaBotBase(object):
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


SUPPORTED_DATABASES = ["mongodb", "elasticsearch"]


class InvanaBot(object):
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

        if database not in ["mongodb", "elasticsearch"]:
            raise Exception("we only support {}".format(",".join(SUPPORTED_DATABASES)))
        #
        # if database == "mongodb":
        #     self.settings['ITEM_PIPELINES'] = {'invana_bot.pipelines.mongodb.MongoDBPipeline': 1}
        #     self.settings['HTTPCACHE_STORAGE'] = "invana_bot.httpcache.mongodb.MongoDBCacheStorage"
        # elif database == "elasticsearch":
        #     self.settings['ITEM_PIPELINES'] = {'invana_bot.pipelines.elasticsearch.ElasticSearchPipeline': 1}
        #     self.settings['HTTPCACHE_STORAGE'] = "invana_bot.httpcache.elasticsearch.ESCacheStorage"
        # elif database == "solr":
        #     self.settings['ITEM_PIPELINES'] = {'invana_bot.pipelines.solr.SolrPipeline': 1}
        #     self.settings['HTTPCACHE_STORAGE'] = "invana_bot.httpcache.solr.SolrCacheStorage"
        # else:
        #     raise Exception("We only support, elasticsearch, solr and mongodb at this moment.")

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
