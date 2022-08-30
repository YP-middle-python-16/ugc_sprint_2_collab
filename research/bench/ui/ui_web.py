import streamlit as st
from benchmark_worker import BenchMark
from benchmark.queue_manager import QueueManager


class ViewUI:
    def __init__(self):
        pass

    def draw(self, onclick):
        st.set_page_config(
            page_title='Engine speed research',
            page_icon='🚀'
        )
        st.title('Engine speed research 🚀')

        with st.form('main_form'):
            tries = st.slider('Number of tries', 0, 100, 10) / 100
            ugc_objects = st.select_slider('Number of tries',
                                           options=[1000, 10000, 100000, 1000000])


            storage_insert = st.multiselect('Insert Storages', key='select1',
                                            options=['Postgres', 'ClickHouse', 'Kafka', 'Mongo', 'Null'])

            storage_select = st.multiselect('Read Storages', key='select2',
                                            options=['Postgres', 'ClickHouse', 'Kafka', 'Mongo', 'Null'])

            submitted = st.form_submit_button('Run Benchmark')

            if submitted:
                if callable(onclick):
                    onclick()
