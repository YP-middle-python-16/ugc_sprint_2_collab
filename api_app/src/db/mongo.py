from typing import Optional

from pymongo import MongoClient

mongo_client: Optional[MongoClient] = None


# Функция понадобится при внедрении зависимостей
async def get_mongo_client() -> MongoClient:
    return mongo_client
