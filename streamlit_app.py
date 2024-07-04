import streamlit as st
from streamlit import session_state
import pandas as pd
from streamlit_scrollable_textbox import scrollableTextbox

import core

# Initializations
session_state.board, session_state.start_pos = core.generate_map()
session_state.commands = list()

# Board and commands
board, command_palette = st.columns([7, 3])

with board:
    st.dataframe(
        pd.DataFrame(
            frontend.visualize(session_state.board),
        ),
        hide_index = True,
        column_config = {i:None for i, _ in enumerate(session_state.board[0])},
        use_container_width = True,
    )

with command_palette:
    scrollableTextbox(frontend.format_commands(session_state.commands))
    if st.button('一歩進む'):
        session_state.commands.append('move')
    if st.button('右を向く'):
        session_state.commands.append('turn')
    if st.button('IF 目の前が壁['):
        session_state.commands.append('if wall')
    if st.button(']ELSE['):
        session_state.commands.append('else')
    if st.button(']'):
        session_state.commands.append('endif')
