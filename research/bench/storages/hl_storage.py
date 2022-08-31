import abc


class HiLoadStorage:
    @abc.abstractmethod
    def __init__(self, connect_param):
        self.label = None
        self.sql_dialect = None

    @abc.abstractmethod
    def insert(self, data=None, query: str = None):
        pass

    @abc.abstractmethod
    def insert_batch(self, data=None, query: str = None):
        pass

    @abc.abstractmethod
    def select(self, data=None, query: str = None):
        pass
