import streamlit as st
from streamlit import session_state
import pandas as pd
from streamlit_scrollable_textbox import scrollableTextbox

import core
import frontend

# Initializations
if 'args' not in session_state:
    session_state.args = {
        'size': (8, 8),
        'complexity_x': 1,
        'complexity_y': 1,
        'flags': 1,
    }
if 'board' not in session_state:
    session_state.board, session_state.start_pos, session_state.flag_positions = core.generate_map(**session_state.args)
if 'commands' not in session_state:
    session_state.commands = list()
if 'executer' not in session_state:
    session_state.executer = None # To show where did the user's program step by step

# Main tab and setting tab
main, setting = st.tabs(['問題', '設定'])

# Board and commands
board, command_palette = st.columns([7, 3])

with main:
    with board:
        st.dataframe(
            pd.DataFrame(
                frontend.visualize(session_state.board),
            ),
            use_container_width = True,
        ) # Static board

        if session_state.executer is not None:
            result = session_state.executer.__next__()
            if isinstance(result, str):
                if '！' in result:
                    st.success(result)
                else:
                    st.error(result)
                session_state.executer = None            

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
        if st.button('実行'):
            session_state.executer = core.execute(session_state.commands, session_state.board, session_state.start_pos)
        if st.button('次へ'):
            session_state.board = core.generate_map(**session_state.args)
            session_state.commands = list()
            session_state.executer = None
            
with setting:
    session_state.args['size'] = (
        st.slider(
            label = '縦の長さ', 
            min_value = 1, 
            max_value = 10, 
            value = 1,
            step = 1,
        ) + 2,
        st.slider(
            label = '横の長さ',
            min_value = 1,
            max_value = 10,
            value = 1,
            step = 1,
        ) + 2,
    )
    session_state.args['complexity_x'] = st.slider(
        label = '縦道の数',
        min_value = 1,
        max_value = session_state.args['size'][1],
        value = 1,
        step = 1,
    )
    session_state.args['complexity_y'] = st.slider(
        label = '横道の数',
        min_value = 1,
        max_value = session_state.args['size'][0],
        value = 1,
        step = 1,
    )
    session_state.args['flags'] = st.slider(
        label = '旗の数',
        min_value = 1,
        max_value = session_state.args['size'][0] * session_state.args['size'][1],
        value = 1,
        step = 1,
    )
