import streamlit as st
from streamlit import session_state
import pandas as pd

from . import core

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
    #
