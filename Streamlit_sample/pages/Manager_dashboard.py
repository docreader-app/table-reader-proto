import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import time
import base64
import os

st.title("Manager Dashboard")

if 'my_list' not in st.session_state:
    st.session_state.my_list = [{"Name": "File1", "Status": "Verifying"}, {"Name": "File2", "Status": "Results Available"}]

col1, col2, col3 = st.columns([9, 9, 3])
with col1:
    st.write("File Name")
with col2:
    st.write("Status")
with col3:
    st.write("Action")

for index, item in enumerate(st.session_state.my_list):
    emp = st.empty()
    col1, col2, col3 = emp.columns([9, 9, 3])
    if item["Status"] == "Results Available":
        if col3.button("Review", key=f"but{index}"):
            st.switch_page("pages/Returned_Result_check.py")
    if len(st.session_state.my_list) > index:
        col1.markdown(f'{item["Name"]}', unsafe_allow_html=True)
        col2.markdown(f'{item["Status"]}', unsafe_allow_html=True)
    else:
        emp.empty()
    
