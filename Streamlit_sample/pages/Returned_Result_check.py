import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer
import time
import base64
import os
import pymupdf

st.set_page_config(layout="wide")

st.title("Here is the result from the Human Verifier(Marked in red color)")

input_ref_pdf_dir = os.path.join("Users/", st.session_state['username'], st.session_state.review_docname, st.session_state.review_docname)
ss.pdf_ref = (pymupdf.open(input_ref_pdf_dir)).tobytes()  # or pymupdf.Document(filename)

def displayPDF():
    # Opening file from file path
    base64_pdf = base64.b64encode(ss.pdf_ref).decode('utf-8')

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
        
        base64_pdf = base64.b64encode(ss.pdf_ref).decode('utf-8')
        pdf_display = f'<iframe width="100%" height="500" src="data:application/pdf;base64,{base64_pdf}#zoom=FitH&view=fit"" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        # displayPDF()
        
    with col2:
        st.header("Human Verified Output")
        
        title_alignment="""
        <style>
        #preliminary-output {
        text-align: center
        }
        </style>    
        """
        st.markdown(title_alignment, unsafe_allow_html=True)
        path = os.path.join("Users/", st.session_state['username'], st.session_state.review_docname, "Annotated_data.csv")
        output = pd.read_csv(path)
        st.dataframe(output, height = 500)        
    col3, col4 = st.columns([15, 15], gap="large")
    with col3:
        if st.button(':blue[Send Back to Worker]', use_container_width=True):
            st.success("Changes requested!")
            st.success("Heading to edit page in 3 seconds")
            time.sleep(3)
            st.switch_page("pages/Additional_Adjustment.py")
    with col4:
        if st.button(':green[Approve]', use_container_width=True):
            st.success("Congratulations! Your data is available!")
            st.success("We will go to the download page in 5 seconds")
            time.sleep(5)
            st.switch_page("pages/Download_page.py")
            


# if uploaded_file is not None:
#     corridors = corridors()
#     st.write(corridors)