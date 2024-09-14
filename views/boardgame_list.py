
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="Board Game - Database", page_icon="♙", layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Database")

df = load_main_dataframe("database")

df = df[['game_id', 'name', 'year', 'minplayers', 'maxplayers', 'playingtime', 'thumbnail', 'url', 'DIY']]
st.warning(df.columns)


cell_renderer = JsCode("""
    class UrlCellRenderer {
        init(params) {
            // Create an anchor element
            this.eGui = document.createElement('a');
            this.eGui.href = params.data.url; // Set the href to the 'url' field in your data
            this.eGui.target = '_blank'; // Optional: Open link in a new tab

            // Create an image element
            var img = document.createElement('img');
            img.src = params.value; // Use the cell value as the image source
            img.height = 100;
            img.style.display = 'block';
            img.style.marginLeft = 'auto';
            img.style.marginRight = 'auto';

            // Append the image to the anchor
            this.eGui.appendChild(img);
        }

        getGui() {
            return this.eGui;
        }
    }
""")



# Configure the 'thumbnail' column to use the built-in image renderer with correct parameters
gb = GridOptionsBuilder.from_dataframe(df)

column_defs = [
    {
        'field': 'thumbnail',
        'headerName': 'Image',
        'cellRenderer': cell_renderer,
        'width': 120
    },
    {
        'field': 'name',
        'headerName': 'Name'
    },
    {
        'field': 'year',
        'headerName': 'Year'
    },
    {
        'field': 'minplayers',
        'headerName': 'Min Players'
    },
    {
        'field': 'maxplayers',
        'headerName': 'Max Players'
    },
    {
        'field': 'url',
        'headerName': 'URL',
        'hide': True  # Hide the 'url' column but keep it in data
    }
]

# Build the grid options
gridOptions = {
    'columnDefs': column_defs,
    'rowHeight': 120  # Adjust the row height as needed
}


AgGrid(
    df,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True
)

