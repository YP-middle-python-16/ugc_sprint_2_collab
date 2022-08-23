import abc


class HiLoadStorage:
    @abc.abstractmethod
    def __init__(self, connect_param):
        pass

    @abc.abstractmethod
    def insert(self, data=None):
        pass

    @abc.abstractmethod
    def insert_batch(self, data=None, batch_size: int = 10):
        pass

    @abc.abstractmethod
    def select(self, data = None):
        pass
