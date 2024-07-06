import streamlit as st
from streamlit import session_state
import numpy as np
import pandas as pd
from streamlit_scrollable_textbox import scrollableTextbox
from time import sleep

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
if 'complexity_x_default' not in session_state:
    session_state['complexity_x_default'] = 1
if 'board' not in session_state:
    session_state.board, session_state.start_pos, session_state.flag_positions = core.generate_map(**session_state.args)
if 'commands' not in session_state:
    session_state.commands = list()
if 'executor' not in session_state:
    session_state.executor = None # To show where did the user's program step by step

# Main tab and setting tab
main, setting = st.tabs(['問題', '設定'])

with main:
    # Board and commands
    board, command_palette = st.columns([7, 3])
    with board:
        st.dataframe(
            frontend.visualize(session_state.board),
            use_container_width = True,
        ) # Static board

        # If the execution process is alive
        if session_state.executor is not None:

            # Advance the player
            try:
                session_state.executor.__next__()

            # Executed all commands
            except StopIteration as e:
                if 0.5 in session_state.board:
                    st.error('失敗...')
                else:
                    st.success('成功！')
                session_state.executor = None   

            # Fell out of the board
            except IndexError as e:
                if 0.5 in session_state.board:
                    st.error('失敗...')
                else:
                    st.success('成功！')
                session_state.executor = None

            # Unknown error
            except Exception as e:
                st.error(f'Unknown error:{e}')
                st.stop()

            # The process not ended yet
            else:
                sleep(1)
                st.rerun()

    with command_palette:
        # Textbox that shows the inputted commands
        scrollableTextbox(frontend.format_commands(session_state.commands))
        
        # Button for inputting command, executing commands, and generating new quiz
        if st.button('一歩進む'):
            session_state.commands.append('move')
            st.rerun()
        if st.button('右を向く'):
            session_state.commands.append('turn')
            st.rerun()
        if st.button('左を向く'):
            session_state.commands.extend(['lturn'])
            st.rerun()
        if st.button('IF 目の前が壁['):
            session_state.commands.append('if wall')
            st.rerun()
        if st.button(']ELSE['):
            session_state.commands.append('else')
            st.rerun()
        if st.button(']'):
            session_state.commands.append('endif')
            st.rerun()
        if st.button('消す'):
            try:
                session_state.commands.pop(-1)
            except IndexError:
                pass
            st.rerun()
        if st.button('実行'):
            # The board should be initialized because a previous execution might have changed the board
            session_state.board = np.where(session_state.board == 0.25, 0, session_state.board)
            session_state.board[session_state.start_pos[0], session_state.start_pos[1]] = 0.25
            for flag_y, flag_x in session_state.flag_positions:
                session_state.board[flag_y, flag_x] = 0.5

            # Ignite the execution process
            session_state.executor = core.execute(session_state.commands, session_state.board, session_state.start_pos)
            st.rerun()
        if st.button('次へ'):
            frontend.rerun()
            st.rerun()
            
with setting:
    st.slider(
            label = '縦の長さ', 
            min_value = 1, 
            max_value = 10, 
            value = session_state.args['size'][0],
            step = 1,
        )
    st.slider(
            label = '横の長さ',
            min_value = 1,
            max_value = 10,
            value = session_state.args['size'][1],
            step = 1,
        )
    st.slider(
        label = '縦道の数',
        min_value = 1,
        max_value = session_state.args['size'][1],
        value = session_state['complexity_x_default'],
        step = 1,
        key = 'complexity_x',
        on_change = frontend.change_default('complexity_x'),
    )
    session_state.args['complexity_y'] = st.slider(
        label = '横道の数',
        min_value = 1,
        max_value = session_state.args['size'][0],
        value = session_state.args['complexity_y'] ,
        step = 1,
    )
    session_state.args['flags'] = st.slider(
        label = '旗の数',
        min_value = 1,
        max_value = min([10, session_state.args['size'][0] * session_state.args['size'][1]]),
        value = session_state.args['flags'],
        step = 1,
    )
