import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
from st_aggrid import AgGrid, GridOptionsBuilder
import time
import base64
import os
import pymupdf
import json


st.set_page_config(layout="wide")
###The following code only works with streamlit data_edit tool.
def highlight_changes(val):
    color = f"color: orange;" if val else "color:lightgray;"
    background = f"background-color:lightgray;" if val else ""
    return f"{color} {background}"

def show_diff(
    source_df: pd.DataFrame, modified_df: pd.DataFrame, editor_key: dict
) -> None:
    target = pd.DataFrame(editor_key.get("edited_rows")).transpose().reset_index()#GET EDITED ROWS!!!
    modified_columns = [i for i in target.notna().columns if i != "index"]
    source = source_df.iloc[target.index].reset_index()
    target = target[modified_columns].reset_index()

    changes = pd.merge(
        source[modified_columns].reset_index(),
        target,
        how="outer",
        on="index",
        suffixes=["_BEFORE", "_AFTER"],
    )
    after_columns = [i for i in changes.columns if "_AFTER" in i]
    for cl in changes:
        if cl in after_columns:
            new_col = cl.replace("_AFTER", "_BEFORE")
            changes[cl] = changes[cl].fillna(changes[new_col])

    st.subheader("Modified")
    st.caption("Showing only modified columns")

    change_markers = changes.copy()
    for cl in change_markers:
        if cl in after_columns:
            new_col = cl.replace("_AFTER", "_BEFORE")
            change_markers[cl] = change_markers[cl] != change_markers[new_col]
            change_markers[new_col] = change_markers[cl]
    st.dataframe(
        changes.style.apply(
            lambda _: change_markers.applymap(highlight_changes), axis=None
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Inserted Rows")
    inserted = pd.DataFrame(editor_key.get("added_rows"))
    st.dataframe(inserted, use_container_width=True)
    st.subheader("Deleted Rows")
    st.dataframe(output.iloc[editor_key.get("deleted_rows")], use_container_width=True)
    
    
###The following code works with AG Grid
# def add_column(Input, ColumnName):
    
    
# def add_row(Input):
#     Input.loc[len(Input.data)] = new_row_list
#     #df3 = pd.concat([df, df2], axis=1)
#     # Display the DataFrame using AgGrid
#     AgGrid(st.session_state.data)


st.write("Change the output by clicking the cell you want to change!")

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
    st.header("Output")
    title_alignment="""
    <style>
    #output {
    text-align: center
    }
    </style>    
    """
    st.markdown(title_alignment, unsafe_allow_html=True)
    path = os.path.join("Users/", st.session_state['username'], st.session_state.review_docname, "Annotated_data.csv")
    output = pd.read_csv(path)
    editor_df = st.data_editor(output, key = "output_edit_ke", height = 500, num_rows="dynamic")
    # AgGrid(output, editable=True)
    # if st.button("Add Row"):
        

    
    
#Functionality needed: make the edited cells lights up with red colors to signal that they are changed!
show_diff(source_df=output, modified_df=editor_df, editor_key=st.session_state["output_edit_ke"])


if st.button(':green[Finish changes]', use_container_width=True):
    st.success("Changes recorded. We will send your data for human verification and will let you know the results once it becomes available!")
    
    Additional_edit_output_csv_dir = os.path.join("Users/", st.session_state['username'], st.session_state.review_docname, 'Additional_Edited_data.csv') 
    editor_df.to_csv(Additional_edit_output_csv_dir)
    
    json_file_path = os.path.join("Users/", st.session_state['username'],'file_list.json')  # File path for storing/retrieving data
    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # File exists, read data from JSON file
        with open(json_file_path, 'r') as file:
            file_list = json.load(file)
    
    new_file_request = {"Name": st.session_state.review_docname, "Status": "Verifying"}
    for index, item in enumerate(st.session_state.my_list):
        if item["Name"] == st.session_state.review_docname:
            item["Status"] = "Verifying"
    
    with open(json_file_path, 'w') as file:
        json.dump(file_list, file)
    
    st.switch_page("pages/Initial_Page.py")