"""
This Pipeline will post the data to the rest api.
"""
from datetime import datetime
import requests
import json
import time


class ApiPipeline(object):
    def __init__(self, api_url=None, headers=None):
        if api_url is None:
            raise Exception("WCP_PIPELINE_API_URL should be provided in the settings "
                            "when using api.ApiPipeline")

        if headers is None:
            headers = {}
        self.headers = headers
        self.api_url = api_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            api_url=crawler.settings.get('WCP_PIPELINE_API_URL'),
            headers=crawler.settings.get('WCP_PIPELINE_API_HEADERS'),
        )

    def clean_data(self, data=None):
        new_data = {}
        if data:
            for k, v in data.items():
                print(type(v))
                if isinstance(v, time.struct_time):
                    v = datetime.fromtimestamp(time.mktime(v))
                new_data[k] = v
            print(new_data)
        return data

    def send(self, data=None):
        if data:
            response = requests.post(self.api_url, data=json.dumps(data, default=str), headers=self.headers)
            print(response.status_code)

    def process_item(self, item, spider):
        data = dict(item)
        data['updated'] = datetime.now()
        data = self.clean_data(data=data)
        self.send(data=data)
        return item
