from pymongo import MongoClient
from core.config import settings


class DocService:
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client
        self.db = self.mongo_client[settings.MONGO_DB]

    async def insert(self, data, table: str):
        data_dict = [dict(row) for row in data]

        collection = self.db[table]
        collection.insert_one(data_dict)

    async def select(self, query: str, table: str):
        query_dict = dict(query)
        collection = self.db[table]

        results = collection.find(query_dict)
        return results

    async def count(self, query: str, table: str):
        query_dict = dict(query)
        collection = self.db[table]

        results = collection.count_documents(query_dict)
        return results
