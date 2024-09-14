
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "link": [
        "https://example.com/alice",
        "https://example.com/bob",
        "https://example.com/charlie",
    ],
}

df = pd.DataFrame(data)
gb = GridOptionsBuilder.from_dataframe(df,
                                        editable=True)

cell_renderer =  JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'SomeText';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)


gb.configure_column(
    "link",
    headerName="link",
    width=100,
    cellRenderer=cell_renderer
)

grid = AgGrid(df,
            gridOptions=gb.build(),
            updateMode=GridUpdateMode.VALUE_CHANGED,
            allow_unsafe_jscode=True)
