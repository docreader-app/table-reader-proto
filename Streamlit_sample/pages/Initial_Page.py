import streamlit as st
from streamlit import session_state as ss
import os
import json

st.title("Data Extraction Prototype")

if st.session_state['username']:
    st.header(f"Welcome, {st.session_state['username']}")
else:
    st.header("Welcome, Guest")

st.header("Hello! Please upload your file, or click Manager Interface to get started!")
    
st.write("This is a prototype. No API has been implemented yet")

#Create the list of dictionaries for storing the data that has been sent for review requests
json_file_path = os.path.join("Users/", st.session_state['username'],'file_list.json')  # File path for storing/retrieving data

# Check if the JSON file exists
if os.path.exists(json_file_path):
    # File exists, read data from JSON file
    with open(json_file_path, 'r') as file:
        file_list = json.load(file)
else:
    # File doesn't exist, create an empty list
    file_list = []
    # Export empty list as JSON file
    with open(json_file_path, 'w') as file:
        json.dump(file_list, file)
        
if 'my_list' not in st.session_state:
    st.session_state.my_list = file_list

#Manager Interface access
if st.button("Manager Interface"):
    st.switch_page("pages/Manager_dashboard.py")

if 'pdf_ref' not in ss:
    ss.pdf_ref = None

#File upload request
uploaded_f = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_f is not None:
    ss.pdf = uploaded_f
    ss.pdf_ref = ss.pdf
    st.switch_page("pages/Initial_Result_check.py")