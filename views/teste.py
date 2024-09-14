
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
            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', "https://fastly.picsum.photos/id/1/200/300.jpg?hmac=jH5bDkLr6Tgy3oAg5khKCHeunZMHq0ehBZr6vGifPLY");
            this.eGui.setAttribute('width', "100");
            this.eGui.setAttribute('height', "100");
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
    height=100,
    cellRenderer=cell_renderer
)

grid = AgGrid(df,
            gridOptions=gb.build(),
            updateMode=GridUpdateMode.VALUE_CHANGED,
            allow_unsafe_jscode=True)
