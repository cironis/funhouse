
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Board Game - Database", page_icon="♙",layout="wide")

st.title("Board Game - Database")

@st.cache_data
def load_main_dataframe(worksheet):

    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df
