
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

df["image_path"] = df["game_id"].apply(lambda x: f"/images/image_{x}.jpg")

render_image = JsCode("""function (params) {
            var element = document.createElement("span");
            var imageElement = document.createElement("img");
        
            if (params.data.image_path) {
                imageElement.src = params.data.image_path;
                imageElement.width="20";
            } else {
                imageElement.src = "";
            }
            element.appendChild(imageElement);
            element.appendChild(document.createTextNode(params.value));
            return element;
            }""")

# Define the function to set row height
get_row_height = JsCode('''
function(params) {
    return 80;
}
''')

# Build grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column('image_path', headerName='Image', cellRenderer=render_image)
gb.configure_column('name', headerName='Name')
gb.configure_column('year', headerName='Year')
gb.configure_column('minplayers', headerName='Min Players')
gb.configure_column('maxplayers', headerName='Max Players')
gb.configure_columns(['playingtime', 'url'], hide=True)
gb.configure_grid_options(getRowHeight=get_row_height)

gridOptions = gb.build()

# Display the grid
AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
