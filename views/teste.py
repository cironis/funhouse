
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
            this.eGui.setAttribute('src', "https://fastly.picsum.photos/id/194/200/200.jpg?hmac=f1VYjvgDG_6vPwJyTb-Xl1HpXKM23stmhFUnmPE_yL8");
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
