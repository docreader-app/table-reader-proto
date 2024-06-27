import streamlit as st
from streamlit import session_state as ss

st.title("Data Extraction Prototype")
st.header("Hello! Please upload your file, or click Manager Interface to get started!")
st.write("This is a prototype. No API has been implemented yet")

if st.button("Manager Interface"):
    st.switch_page("pages/Manager_dashboard.py")

if 'pdf_ref' not in ss:
    ss.pdf_ref = None

uploaded_f = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_f is not None:
    ss.pdf = uploaded_f
    ss.pdf_ref = ss.pdf
    st.switch_page("pages/Initial_Result_check.py")