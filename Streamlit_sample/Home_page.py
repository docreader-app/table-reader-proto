import streamlit as st
from streamlit import session_state as ss
import pandas as pd

st.title("Data Extraction Prototype")

if 'pdf_ref' not in ss:
    ss.pdf_ref = None

uploaded_f = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_f is not None:
    ss.pdf = uploaded_f
    ss.pdf_ref = ss.pdf