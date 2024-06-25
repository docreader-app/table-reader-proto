import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
from st_aggrid import AgGrid, GridOptionsBuilder
import time
import base64
import os

st.title("Manager Dashboard")

