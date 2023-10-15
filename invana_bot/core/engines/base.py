from invana_bot.transformers.mongodb import OTManager, ReadFromMongo, WriteToMongoDB
from twisted.internet import reactor
import requests
import logging

logger = logging.getLogger(__name__)


class RunnerEngineBase(object):
    """

    RunnerEngineBase

    """

    def run(self):
        return self.crawl()

    def get_index(self, storage_id=None, data_storages=None):

        data_storages = self.manifest.get('datasets', [])
        for _index in data_storages:
            if _index['storage_id'] == storage_id:
                return _index

    def get_default_index(self, data_storages=None):
        for _index in data_storages:
            if _index['storage_id'] == "default":
                return _index

    def index_transformed_data(self, index=None, results_cleaned=None):
        collection_name = index['collection_name']
        unique_key_field = index['unique_key']

        mongo_executor = WriteToMongoDB(
            index['connection_uri'],
            index['database_name'],
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

    def callback(self, callback_fn=None):
        all_data_storages = self.manifest.get('datasets', [])
        if len(all_data_storages) == 0:
            print("There are no callback notifications associated with the indexing jobs. So we are Done here.")
        else:
            print("Initiating, sending the callback notifications after the respective transformations ")
            for index in all_data_storages:
                data_storage_id = index.get('data_storage_id')
                callback_config = self.get_callback_for_index(data_storage_id=data_storage_id)
                if callback_config:
                    try:
                        self.trigger_callback(callback_config=callback_config)
                    except Exception as e:
                        print("Failed to send callback[{}] with error: {}".format(callback_config.get("callback_id"),
                                                                                  e))

        if callback_fn is None:
            reactor.stop()
        else:
            callback_fn()

    def get_callback_for_index(self, data_storage_id=None):
        callbacks = self.manifest.get("callbacks", [])
        for callback in callbacks:
            callback_data_storage_id = callback.get('data_storage_id')
            if callback_data_storage_id == data_storage_id:
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
            storage_id = transformation.get('storage_id')

            transformation_index_config = self.get_index(storage_id=storage_id)
            default_storage = self.get_index(storage_id="default")
            print("transformation_index_config", transformation_index_config)
            # read data from default storage
            mongo_executor = ReadFromMongo(
                default_storage['connection_uri'],
                default_storage['database_name'],
                default_storage['collection_name'],
                query={"context.job_id": self.job_id}
            )
            mongo_executor.connect()
            ops = []
            ot_manager = OTManager(ops).process(mongo_executor)
            results = ot_manager.results
            try:
                results_cleaned__ = transformation_fn(results)
                logger.info("Finished the transformation with transformation_id : {}".format(transformation_id))
            except Exception as e:
                logger.error(
                    "Failed the transformation with transformation_id : {} with error :: {}".format(transformation_id,
                                                                                                    e))
                results_cleaned__ = []
            results_cleaned = []
            for result in results_cleaned__:
                if "_id" in result.keys():
                    del result['_id']
                if "context" in result.keys():
                    result['context']['job_id'] = self.job_id
                else:
                    result['context'] = {'job_id': self.job_id}

                results_cleaned.append(result)
            self.index_transformed_data(index=transformation_index_config, results_cleaned=results_cleaned)

            print("Total results_cleaned count of job {} is {}".format(self.job_id, results_cleaned.__len__()))

        print("======================================================")
        print("Successfully crawled + transformed + indexed the data.")
        print("======================================================")
        self.callback(callback_fn=callback_fn)
