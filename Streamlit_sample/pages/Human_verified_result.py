import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
from st_aggrid import AgGrid, GridOptionsBuilder
import time
import base64
import os

st.set_page_config(layout="wide")

def highlight_changes(val):
    color = f"color: orange;" if val else "color:lightgray;"
    background = f"background-color:lightgray;" if val else ""
    return f"{color} {background}"
    
st.title("Human verified results")

col1, col2 = st.columns([15, 15], gap="large")
with col1:
    st.header("Your PDF File")
    
    title_alignment="""
    <style>
    #your-pdf-file {
    text-align: center
    }
    </style>    
    """
    st.markdown(title_alignment, unsafe_allow_html=True)
        
    base64_pdf = base64.b64encode(ss.pdf_ref.getvalue()).decode('utf-8')
    pdf_display = f'<iframe width="100%" height="500" src="data:application/pdf;base64,{base64_pdf}#zoom=FitH&view=fit"" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    # displayPDF()
        
with col2:
    st.header("Human verified results")
    title_alignment="""
    <style>
    #human-verified-results {
    text-align: center
    }
    </style>    
    """
    st.markdown(title_alignment, unsafe_allow_html=True)
    path = os.path.join("pages", "output.xlsx")
    output = pd.read_excel(path)
    editor_df = st.data_editor(output, key = "output_edit_ke", height = 500, num_rows="dynamic")
    
    st.write("Need to work on:")
    st.write("1. Highlight the changes made by both manager and the human verifier, in two different colors\n2. Algorithm that allow it to show the changes fast")