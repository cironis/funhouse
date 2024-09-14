
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="Test Image Rendering", layout="wide")

# Create a simple DataFrame with a known image URL
test_df = pd.DataFrame({
    'thumbnail': ['https://via.placeholder.com/50'],
    'name': ['Test Game'],
    'year': [2021],
    'minplayers': [2],
    'maxplayers': [4],
    'url': ['https://example.com']
})

# Define the custom renderer
render_image = JsCode('''
    function renderImage(params) {
        return `<img src="${params.value}" width="50" height="50" />`;
    }
''')

# Configure the grid
gb = GridOptionsBuilder.from_dataframe(test_df)
gb.configure_column(
    'thumbnail',
    headerName='Image',
    cellRenderer=render_image,
    width=100
)
gb.configure_column('name', headerName='Name')
gb.configure_column('year', headerName='Year')
gb.configure_column('minplayers', headerName='Min Players')
gb.configure_column('maxplayers', headerName='Max Players')
gb.configure_column('url', headerName='URL', hide=True)
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
    test_df,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True
)
