
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


st.set_page_config(page_title="Board Game - Database", page_icon="♙",layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):

    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Board Game - Database")

df = load_main_dataframe("database")

# Define the cell renderer to display image as a hyperlink
cell_renderer = JsCode('''
function(params) {
    return '<a href="' + params.data.url + '" target="_blank"><img src="' + params.data.image_path + '" style="height:60px;"></a>';
}
''')

# Define the function to set row height
get_row_height = JsCode('''
function(params) {
    return 80;
}
''')

# Build grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column('image_path', headerName='Image', cellRenderer=cell_renderer)
gb.configure_column('name', headerName='Name')
gb.configure_column('year', headerName='Year')
gb.configure_column('minplayers', headerName='Min Players')
gb.configure_column('maxplayers', headerName='Max Players')
gb.configure_columns(['playingtime', 'url'], hide=True)
gb.configure_grid_options(getRowHeight=get_row_height)

gridOptions = gb.build()

# Display the grid
AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
