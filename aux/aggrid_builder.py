
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

def create_grid(df,selection):

    hide = not selection

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
            'cellRenderer': cell_renderer,
            'flex': 1,
            'minWidth': 100,
            'maxWidth': 200,
        },
        {
            'field': 'name',
            'headerName': 'Name',
            'flex': 2
        },
        {
            'field': 'year',
            'headerName': 'Year',
            'flex': 0.5
        },
        {
            'field': 'minplayers',
            'headerName': 'Min Players',
            'flex': 0.5
        },
        {
            'field': 'maxplayers',
            'headerName': 'Max Players',
            'flex': 0.5
        },
        {
            'field': 'playingtime',
            'headerName': 'Playing Time (min)',
            'flex': 0.5
        },
        {
            'field': 'url',
            'headerName': 'URL',
            'hide': True  # Hide the 'url' column but keep it in data
        },
        {
            'field': 'game_id',
            'headerName': 'game_id',
            'hide': True,
        },
        {
            'headerName': 'Add to Database',
            'hide': hide,
            'checkboxSelection': selection
        }
    ]

    # Build the grid options
    gridOptions = {
        'columnDefs': column_defs,
        'rowHeight': 120
    }

    if (selection == True):
        grid = AgGrid(
            df,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            theme="material",
            update_mode=GridUpdateMode.SELECTION_CHANGED
        )
    else:
        grid = AgGrid(
            df,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            theme="material"
        )

    return grid
