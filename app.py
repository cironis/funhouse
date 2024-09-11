import streamlit as st

# --- PAGE SETUP ---
boardgame_page = st.Page(
    "views/boardgame_list.py",
    title="Lista de Boardgames",
    icon=":material/thumb_up:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Boardgames": [boardgame_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")

# --- RUN NAVIGATION ---
pg.run()
