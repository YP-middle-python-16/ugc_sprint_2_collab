from benchmark.timeit import timeit
from ugc.ugc import ucg_config
from ugc.ugc_provider import UGCProvider
from storages.hl_storage import HiLoadStorage


class Worker:
    def __init__(self, ugc_provider, storage_service: HiLoadStorage, mode: str = 'single'):
        self.ucg_provider: UGCProvider = ugc_provider()
        self.storage_service: HiLoadStorage = storage_service
        self.sql_dialect = storage_service.sql_dialect
        self.data = []
        self.mode = mode

    def prepare_data_insert(self):
        for row in self.ucg_provider.generate(ucg_config.OBJECTS_MAX_LIM):
            self.data.append(row)

    def prepare_data_select(self):
        pass

    def run_insert_single(self):
        if self.sql_dialect:
            for row in self.data:
                query = self.ucg_provider.get_insert_query(row, self.sql_dialect)
                self.storage_service.insert(row, query)
        else:
            for row in self.data:
                self.storage_service.insert(row)

    def run_insert_batch(self):
        if self.sql_dialect:
            query = self.ucg_provider.get_insert_query_batch(self.data, self.sql_dialect)
            self.storage_service.insert_batch(self.data, query)
        else:
            self.storage_service.insert_batch(self.data)

    @timeit
    def run_insert(self):
        if self.mode == 'single':
            self.run_insert_single()

        if self.mode == 'batch':
            self.run_insert_batch()

    @timeit
    def run_select(self):
        pass
