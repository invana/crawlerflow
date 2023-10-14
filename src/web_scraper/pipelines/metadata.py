import json
from itemadapter import ItemAdapter
import datetime


class MetadataPipeline:
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['meta__ingested_at'] = datetime.datetime.now()
        return item