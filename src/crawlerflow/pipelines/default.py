from datetime import datetime
from scrapy.exceptions import DropItem
from pymongo import MongoClient


class WebScraperPipeline(object):

    @staticmethod
    def create_mongodb_connection(data_storage=None):
        db_client = MongoClient(data_storage.get("connection_uri"))
        db_conn = db_client[data_storage.get("database_name")]
        return db_conn
 
    def __init__(self, data_storages=None):

        self.data_storage_conns = {}
        for data_storage in data_storages:
            storage_type = data_storage.get("storage_type", "mongodb")
            storage_id = data_storage.get("storage_id", "default")
            if storage_type == "mongodb":
                self.data_storage_conns[storage_id] = {
                    "_connection": self.create_mongodb_connection(data_storage=data_storage),
                    "_data_storage": data_storage
                }
 
            else:
                raise NotImplementedError("yet to implement '{}' pipeline".format(storage_type))

    @classmethod
    def from_crawler(cls, spider):
        return cls(
            data_storages=spider.spider.manifest.get("datasets")
        )

    def process_item(self, item, spider):
        """

        :param item:  {
            "_data_storage_id": "default",
            "_data_storage_collection_name": "mycollection",
            "_data": <data to save>
        }
        :param spider:
        :return:
        """
        """
        comes handy during the custom data saving.

        data_storage_id = item.get("_data_storage_id")

        """
        data_storage_id = "default"
        data_storage = self.data_storage_conns.get(data_storage_id)
        data_storage_conn = data_storage.get("_connection")
        data_storage_collection_name = data_storage.get("_data_storage", {}).get("collection_name")

        data = item.get("_data")
        if None in [data_storage, data_storage_conn]:
            raise DropItem(
                "Data storage with id: {} doesn't exist, so dropping the item {}".format(data_storage_id, item))

        data = dict(data)
        if "updated" not in data.keys():
            data['updated'] = datetime.now()
        data_storage_type = data_storage.get("storage_type") or "mongodb"
        if data_storage_type == "mongodb":
            data_storage_conn[data_storage_collection_name].insert(data)
        else:
            raise NotImplementedError(
                "storage_type:{} not implemeneted, so extracted data is not saved.".format(data_storage_type))

        return item
