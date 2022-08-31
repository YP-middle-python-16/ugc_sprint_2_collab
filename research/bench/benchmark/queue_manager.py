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
        engine_caption = st.caption(f'Insert into...')

        cols_labels = ('Engine', 'Insert time')
        bench_data = []

        for worker in self.workers:
            engine_caption.caption(f'Insert into {worker.storage_service.label}')
            my_bar.progress(0)

            worker_time = 0
            for i in range(ucg_config.BATCHES):
                current_time, result = worker.run_insert()
                worker_time = worker_time + current_time

                my_bar.progress((i + 1) / ucg_config.BATCHES)

            worker_statistics = [worker.storage_service.label, worker_time]
            bench_data.append(worker_statistics)

        engine_caption.caption('')
        my_bar.progress(0)

        df = pd.DataFrame(bench_data, columns=cols_labels)
        st.table(df)

    def run(self):
        self.prepare_workers()
        self.run_workers()
