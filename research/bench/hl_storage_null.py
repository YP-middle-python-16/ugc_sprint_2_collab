from hl_storage_abstract import HiLoadStorage


class DevNullStorage(HiLoadStorage):
    def __init__(self, connect_param = None):
        pass

    def insert(self, data=None):
        pass

    def insert_batch(self, data=None, batch_size: int = 10):
        pass

    def select(self, data=None):
        pass