import abc


class UGCProvider:
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate(self, limit:int):
        pass

    @abc.abstractmethod
    def get_insert_query(self, data, sql_dialect):
        pass

    @abc.abstractmethod
    def get_insert_query_batch(self, data, sql_dialect):
        pass

    @abc.abstractmethod
    def get_select_query(self, data, sql_dialect):
        pass
