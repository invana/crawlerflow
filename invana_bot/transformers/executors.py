from pymongo import MongoClient


class Executor:
    def connect(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError
