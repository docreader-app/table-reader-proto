import streamlit as st 
import pandas as pd

st.set_page_config(layout="wide")

st.title("Your Data is here!")

def convert_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

title_alignment="""
<style>
#your-data-is-here {
text-align: center
}
</style>    
"""
st.markdown(title_alignment, unsafe_allow_html=True)

output = pd.read_excel("pages/output.xlsx")
st.dataframe(output, height = 500)  

st.download_button(":green[Download CSV]", convert_csv(output), file_name="output_df.csv", use_container_width = True)
