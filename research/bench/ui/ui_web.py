import streamlit as st
from ugc.ugc import ucg_config
from benchmark.stotages_cataloge import STORAGES_CATALOG


class ViewUI:
    def __init__(self):
        pass

    def draw(self, onclick):
        st.set_page_config(
            page_title='Engine speed research',
            page_icon='🚀'
        )
        st.title('Engine speed research 🚀')

        storage_labels = []

        for item in STORAGES_CATALOG:
            if STORAGES_CATALOG[item]['use']:
                storage_name = STORAGES_CATALOG[item]['storage']
                storage_labels.append(storage_name)

        with st.form('main_form'):
            tries = st.slider('Number of cycles in bench', 1, 100, 10)
            ugc_objects = st.select_slider('Number of UGC Objects in one cycle',
                                           options=[10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000,
                                                    1000000])

            storage = st.multiselect('Insert Storages', key='select1',
                                     options=storage_labels)

            submitted = st.form_submit_button('Run Benchmark')

            if submitted:
                if callable(onclick):
                    ucg_config.BATCHES = int(tries)
                    ucg_config.OBJECTS_MAX_LIM = int(ugc_objects)

                    onclick()
