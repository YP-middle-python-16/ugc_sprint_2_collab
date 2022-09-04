from storages.hl_storage import HiLoadStorage
from pymongo import MongoClient
import pymongo


class MongoDBStorage(HiLoadStorage):
    def __init__(self, connect_param=None):
        self.sql_dialect = 'mongo'
        self.label = 'Mongo'

        CONNECTION_STRING = "mongodb://root:example@localhost/"

        self.client = MongoClient(connect_param)
        self.db = self.client['SeriesDB']

        # Fetch our series collection
        # series_collection = self.db['series']

    def insert(self, data=None, query: str = None):
        data_dict = dict(data)

        collection = self.db[query]
        collection.insert_one(data_dict)

    def insert_batch(self, data=None, query: str = None):
        data_dict = [dict(row) for row in data]

        collection = self.db[query]
        collection.insert_many(data_dict)

    def select(self, data=None, query: str = None):
        collection = self.db[query]
        results = collection.find(query)
        return [r for r in results]
