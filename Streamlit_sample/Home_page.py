import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth
import pandas as pd
from supabase import create_client, Client
from st_login_form import login_form

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

client = login_form()

if st.session_state["authenticated"]:
    if st.session_state["username"]:
        st.success(f"Welcome {st.session_state['username']}")
        st.switch_page("pages/Initial_Page.py")
    else:
        st.success("Welcome guest")
        st.switch_page("pages/Initial_Page.py")
else:
    st.error("Not authenticated")