
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from aux.aggrid_builder import create_grid

st.set_page_config(page_title="Board Game - Database", page_icon="♙", layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Database")

df = load_main_dataframe("database")
total_de_jogos = len(df)

# columns ['game_id', 'name', 'year', 'minplayers', 'maxplayers', 'playingtime', 'thumbnail', 'url', 'DIY']
filter_1,filter_2 = st.columns(2)

with filter_1:
    num_players = st.number_input("Number of players",step=1,placeholder="Number of players",value=2)

with filter_2:
    diy_filter = st.selectbox("DIY",["Todos","Sim","Não"])

if num_players is not None:
    df = df.loc[(df['minplayers'] <= num_players) & (df['maxplayers'] >= num_players)]

if diy_filter != "Todos":
    if diy_filter == "Sim":
        df = df[df['DIY'] == True]
    else:
        df = df[df['DIY'] == False]

create_grid(df,False)

jogos_filtrados = len(df)
st.write(f"Jogos: {jogos_filtrados}/{total_de_jogos}")
