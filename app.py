#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Sorteador",
    page_icon="☘️",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Title
st.title("☘️ Sorteador")

def teste_write():
    st.write("The current movie title is", title)

title = st.text_input("Movie title", on_change=teste_write)
