import streamlit as st
import pandas as pd

from benchmark.stotages_cataloge import STORAGES_CATALOG
from ugc.ugc import ucg_config
from ugc import UCG_PROVIDERS
from benchmark.worker import Worker


class QueueManager:
    def __init__(self):
        self.services = {}
        self.ugc_data = {}
        self.workers: list[Worker] = []

        self.my_bar = st.progress(0)
        self.engine_caption = st.caption(f'Insert into...')

    def prepare_workers(self):
        self.engine_caption.caption(f'Prepare data')
        self.my_bar.progress(0)

        self.workers = []
        for item in STORAGES_CATALOG:
            if STORAGES_CATALOG[item]['use']:
                mode = STORAGES_CATALOG[item]['mode']
                storage_name = STORAGES_CATALOG[item]['storage']

                for ugc_label in UCG_PROVIDERS:
                    ugc_provider = UCG_PROVIDERS[ugc_label]
                    storage_service = STORAGES_CATALOG[item]['client']

                    tmp_worker = Worker(ugc_provider, storage_service, mode)
                    self.workers.append(tmp_worker)

    def run_workers(self):
        bench_data = []

        for worker in self.workers:
            worker.prepare_data()
            insert_time = self.insert_cycle(worker)
            select_time = self.select_cycle(worker)

            worker_statistics = [worker.storage_service.label, insert_time, select_time]
            bench_data.append(worker_statistics)

        self.engine_caption.caption('')
        self.my_bar.progress(0)

        cols_labels = ('Engine', 'Insert time\n(less in better)', 'Select time\n(less in better)')
        df = pd.DataFrame(bench_data, columns=cols_labels)
        st.table(df)

    def insert_cycle(self, worker):
        self.engine_caption.caption(f'Insert into {worker.storage_service.label}')
        self.my_bar.progress(0)
        total_time_insert = 0
        for i in range(ucg_config.BATCHES):
            time_insert, result = worker.run_insert()
            total_time_insert = total_time_insert + time_insert

            self.my_bar.progress((i + 1) / ucg_config.BATCHES)

        return total_time_insert

    def select_cycle(self, worker):
        self.engine_caption.caption(f'Select into {worker.storage_service.label}')
        self.my_bar.progress(0)
        total_time_select = 0
        for i in range(ucg_config.BATCHES):
            time_select, result = worker.run_select()
            total_time_select = total_time_select + time_select

            self.my_bar.progress((i + 1) / ucg_config.BATCHES)

        return total_time_select

    def run(self):
        self.prepare_workers()
        self.run_workers()
