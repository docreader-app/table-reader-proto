import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer
import time
import base64
import os

st.set_page_config(layout="wide")

def displayPDF():
    # Opening file from file path
    base64_pdf = base64.b64encode(ss.pdf_ref.getvalue()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100%;">"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

if ss.pdf_ref:
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
        st.header("Preliminary output")
        
        title_alignment="""
        <style>
        #preliminary-output {
        text-align: center
        }
        </style>    
        """
        st.markdown(title_alignment, unsafe_allow_html=True)
        path = os.path.join("pages", "output.xlsx")
        output = pd.read_excel(path)
        st.dataframe(output, height = 500)        
    col3, col4 = st.columns([15, 15], gap="large")
    with col3:
        if st.button(':blue[Request Human Verification]', use_container_width=True):
            st.success("Human verification requested. We will inform you the result once it becomes available!")
            st.success("We will return to the home page in 5 seconds")
            time.sleep(5)
            st.switch_page("pages/Initial_Page.py")
    with col4:
        if st.button(':green[Approve]', use_container_width=True):
            st.success("Congratulations! Your data is available!")
            st.success("We will go to the download page in 5 seconds")
            time.sleep(5)
            st.switch_page("pages/Download_page.py")
            


# if uploaded_file is not None:
#     corridors = corridors()
#     st.write(corridors)