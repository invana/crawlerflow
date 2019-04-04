from scrapy.linkextractors import LinkExtractor
from invana_bot.utils.crawlers import get_crawler_from_list
# from invana_bot.runners.single import SingleCrawlerRunner
from invana_bot.utils.config import validate_cti_config
from transformers.transforms import OTManager
from transformers.executors import ReadFromMongo
from invana_bot.transformers.mongodb import WriteToMongoDB
from invana_bot.transformers.default import default_transformer
import requests


class RunnerBase(object):

    def run(self):
        return self.crawl()

    @staticmethod
    def get_index(transformation_id=None, indexes=None):
        for _index in indexes:
            if _index['transformation_id'] == transformation_id:
                return _index

    def index_data(self, index=None, results_cleaned=None):
        collection_name = index['collection_name']
        unique_key_field = index['unique_key']
        mongo_executor = WriteToMongoDB(
            self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['CONNECTION_URI'],
            self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['DATABASE_NAME'],
            collection_name,
            unique_key_field,
            docs=results_cleaned)
        mongo_executor.connect()
        mongo_executor.write()

    def trigger_callback(self, callback_config=None):
        callback_id = callback_config.get("callback_id")
        print("Triggering callback_id: {}".format(callback_id))

        url = callback_config.get("url")
        request_type = callback_config.get("request_type", '').lower()
        if request_type == "get":
            req = requests.get(url, headers=callback_config.get("headers", {}), verify=False)
            response = req.text
            print("Triggered callback successfully and callback responded with message :{}".format(response))
        elif request_type == "post":
            req = requests.post(url, json=callback_config.get("payload", {}),
                                headers=callback_config.get("headers", {}), verify=False)
            response = req.text
            print("Triggered callback successfully and callback responded with message :{}".format(response))

    def callback(self):
        all_indexes = self.manifest.get('indexes', [])
        if len(all_indexes) == 0:
            print("There are no callback notifications associated with the indexing jobs. So we are Done here.")
        else:
            print("Initiating, sending the callback notifications after the respective transformations ")
            for index in all_indexes:
                index_id = index.get('index_id')
                callback_config = self.get_callback_for_index(index_id=index_id)
                if callback_config:
                    try:
                        self.trigger_callback(callback_config=callback_config)
                    except Exception as e:
                        print("Failed to send callback[{}] with error: {}".format(callback_config.get("callback_id"),
                                                                                  e))

    def get_callback_for_index(self, index_id=None):
        callbacks = self.manifest.get("callbacks", [])
        for callback in callbacks:
            callback_index_id = callback.get('index_id')
            if callback_index_id == index_id:
                return callback
        return

    def transform_and_index(self, callback_fn=None):
        """
        This function will handle both tranform and index

        :param callback:
        :return:
        """
        print("transformer started")

        all_transformation = self.manifest.get('transformations', [])

        for transformation in all_transformation:
            print("transformation", transformation)
            transformation_id = transformation['transformation_id']
            transformation_fn = transformation.get('transformation_fn')

            transformation_index_config = self.get_index(transformation_id=transformation_id,
                                                         indexes=self.manifest['indexes'])
            mongo_executor = ReadFromMongo(
                self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['CONNECTION_URI'],
                self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['DATABASE_NAME'],
                self.settings['INVANA_BOT_SETTINGS']['ITEM_PIPELINES_SETTINGS']['COLLECTION_NAME'],
                query={"context.job_id": self.job_id}
            )
            mongo_executor.connect()
            ops = []
            ot_manager = OTManager(ops).process(mongo_executor)
            results = ot_manager.results
            results_cleaned__ = transformation_fn(results)
            results_cleaned = []
            for result in results_cleaned__:
                if "_id" in result.keys():
                    del result['_id']
                if "context" in result.keys():
                    result['context']['job_id'] = self.job_id
                else:
                    result['context'] = {'job_id': self.job_id}

                results_cleaned.append(result)
            self.index_data(index=transformation_index_config, results_cleaned=results_cleaned)

            print("Total results_cleaned count of job {} is {}".format(self.job_id, results_cleaned.__len__()))

        print("======================================================")
        print("Successfully crawled + transformed + indexed the data.")
        print("======================================================")
        self.callback()
        if callback_fn:
            callback_fn()
