import streamlit as st

from benchmark.stotages_cataloge import STORAGES_CATALOG
from ugc.ugc import ucg_config
from ugc import UCG_PROVIDERS
from benchmark.worker import Worker


class QueueManager:
    def __init__(self):
        self.services = {}
        self.ugc_data = {}
        self.workers: list[Worker] = []

    def prepare_workers(self):
        self.workers = []
        for item in STORAGES_CATALOG:
            if STORAGES_CATALOG[item]['use']:
                mode = STORAGES_CATALOG[item]['mode']
                storage_name = STORAGES_CATALOG[item]['storage']

                for ugc_label in UCG_PROVIDERS:
                    ugc_provider = UCG_PROVIDERS[ugc_label]
                    storage_service = STORAGES_CATALOG[item]['client']

                    tmp_worker = Worker(ugc_provider, storage_service, mode)
                    tmp_worker.prepare_data_insert()
                    self.workers.append(tmp_worker)

    def run_workers(self):
        my_bar = st.progress(0)

        for worker in self.workers:
            for i in range(ucg_config.BATCHES):
                worker.run_insert()
                my_bar.progress(i/ucg_config.BATCHES)

    def run(self):
        self.prepare_workers()
        self.run_workers()