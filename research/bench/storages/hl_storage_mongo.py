from storages.hl_storage import HiLoadStorage


class MongoStorage(HiLoadStorage):
    def __init__(self, connect_param=None):
        self.sql_dialect = 'mongo'

    def insert(self, data=None):
        pass

    def insert_batch(self, data=None, batch_size: int = 10):
        pass

    def select(self, data=None):
        pass
