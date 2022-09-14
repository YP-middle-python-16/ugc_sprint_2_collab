from pymongo import MongoClient
from models.models import EventMessage
from core.config import settings
from core.config import settings


class DocService:
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client
        self.db = self.mongo_client[settings.MONGO_DB]

    async def insert(self, data, table: str):
        data_dict = dict(data)

        collection = self.db[table]
        doc_id = collection.insert_one(data_dict).inserted_id

        return doc_id

    async def select(self, query, table: str):
        collection = self.db[table]
        return [doc for doc in collection.find(query)]

    async def view_all(self, table: str):
        collection = self.db[table]
        return [doc for doc in collection.find()]

    async def count(self, query , table: str):
        collection = self.db[table]
        return collection.count_documents(query)
