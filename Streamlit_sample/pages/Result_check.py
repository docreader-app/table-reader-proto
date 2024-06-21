import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer
import base64

if ss.pdf_ref:
    base64_pdf = base64.b64encode(ss.pdf_ref.getvalue()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



# if uploaded_file is not None:
#     corridors = corridors()
#     st.write(corridors)