
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

# columns ['game_id', 'name', 'year', 'minplayers', 'maxplayers', 'playingtime', 'thumbnail', 'url', 'DIY']
filter_1,filter_2 = st.columns(2)

with filter_1:
    num_players = st.number_input("Number of players",step=1,min_value=1,placeholder="Number of players",value=2)

with filter_2:
    diy_filter = st.selectbox("DIY",["Todos","Sim","Não"])

if num_players is not None:
    df = df.loc[(df['minplayers'] <= num_players) & (df['maxplayers'] >= num_players)]

if diy_filter != "Todos":
    if diy_filter == "Sim":
        df = df[df['DIY'] == True]
    else:
        df = df[df['DIY'] == False]

grid = create_grid(df)
grid

# cell_renderer = JsCode("""
#     class UrlCellRenderer {
#         init(params) {
#             // Create an anchor element
#             this.eGui = document.createElement('a');
#             this.eGui.href = params.data.url; // Set the href to the 'url' field in your data
#             this.eGui.target = '_blank'; // Optional: Open link in a new tab

#             // Create an image element
#             var img = document.createElement('img');
#             img.src = params.value; // Use the cell value as the image source
#             img.height = 100;
#             img.style.display = 'block';
#             img.style.marginLeft = 'auto';
#             img.style.marginRight = 'auto';

#             // Append the image to the anchor
#             this.eGui.appendChild(img);
#         }

#         getGui() {
#             return this.eGui;
#         }
#     }
# """)



# # Configure the 'thumbnail' column to use the built-in image renderer with correct parameters
# gb = GridOptionsBuilder.from_dataframe(df)

# column_defs = [
#     {
#         'field': 'thumbnail',
#         'headerName': 'Image',
#         'cellRenderer': cell_renderer
#     },
#     {
#         'field': 'name',
#         'headerName': 'Name',
#         'flex': 2
#     },
#     {
#         'field': 'year',
#         'headerName': 'Year'
#     },
#     {
#         'field': 'minplayers',
#         'headerName': 'Min Players'
#     },
#     {
#         'field': 'maxplayers',
#         'headerName': 'Max Players'
#     },
#     {
#         'field': 'playingtime',
#         'headerName': 'Playing Time (min)'
#     },
#     {
#         'field': 'url',
#         'headerName': 'URL',
#         'hide': True  # Hide the 'url' column but keep it in data
#     }
# ]

# # Build the grid options
# gridOptions = {
#     'columnDefs': column_defs,
#     'rowHeight': 120
# }

# on_grid_ready = JsCode("""
# function(event) {
#     event.api.sizeColumnsToFit();
# }
# """)

# gridOptions['onGridReady'] = on_grid_ready


# AgGrid(
#     df,
#     gridOptions=gridOptions,
#     allow_unsafe_jscode=True,
#     fit_columns_on_grid_load=True,
#     theme="material"
# )

