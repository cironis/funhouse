
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

def create_grid(df,selection):

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
    
    if (selection == True):
        gb.configure_selection('single', use_checkbox=True)

    column_defs = [
        {
            'field': 'thumbnail',
            'headerName': 'Image',
            'cellRenderer': cell_renderer
            'checkboxSelection': True
        },
        {
            'field': 'name',
            'headerName': 'Name',
            'flex': 2
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
            'field': 'playingtime',
            'headerName': 'Playing Time (min)'
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
        'rowHeight': 120
    }

    on_grid_ready = JsCode("""
    function(event) {
        event.api.sizeColumnsToFit();
    }
    """)

    gridOptions['onGridReady'] = on_grid_ready


    if (selection == True):
        grid = AgGrid(
            df,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
            theme="material",
            update_mode=GridUpdateMode.SELECTION_CHANGED 
        )
    else:
        grid = AgGrid(
            df,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
            theme="material"
        )

    return grid
