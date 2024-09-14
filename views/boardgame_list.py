
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

st.title("Board Game - Database")

df = load_main_dataframe("database")

render_image = JsCode('''
                      
    function renderImage(params) {
    // Create a new image element
    var img = new Image();

    // Set the src property to the value of the cell (should be a URL pointing to an image)
    img.src = params.value;

    // Set the width and height of the image to 50 pixels
    img.width = 50;
    img.height = 50;

    // Return the image element
    return img;
    }
'''
)


# Configure the 'thumbnail' column to use 'agImageCellRenderer'
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column(
    'thumbnail',
    headerName='Image',
    cellRenderer='render_image',
    width=100
)

gb.configure_column('name', headerName='Name')
gb.configure_column('year', headerName='Year')
gb.configure_column('minplayers', headerName='Min Players')
gb.configure_column('maxplayers', headerName='Max Players')
gb.configure_columns(['playingtime', 'url'], hide=True)
gb.configure_grid_options(
    getRowHeight=JsCode('function(params) { return 80; }')
)

# Define the onCellClicked event
on_cell_clicked = JsCode('''
function(event) {
    if (event.colDef.field === 'thumbnail') {
        window.open(event.data.url, '_blank');
    }
}
''')

gridOptions = gb.build()
gridOptions['onCellClicked'] = on_cell_clicked

# Display the grid
AgGrid(
    df,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True
)
