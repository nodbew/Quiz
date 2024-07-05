import numpy as np
import streamlit as st

import core


def visualize(board:np.ndarray) -> np.ndarray:
    '''
    Takes an ndarray that represents the board.
    It should consist with 0, 1, 0.5, 0.25.
    0 should represent a walkable area, 
    1 for a wall,
    0.5 for a flag, and
    0.25 for a player.

    0 will be converted into '',
    1 to 'X',
    0.5 to :checkered_flag:,
    and 0.25 to ':cat:'.
    '''
    shape = board.shape
    board = board.copy().as_dtype('U')
    conditions = [board == 0, board == 1, board == 0.5, board == 0.25]
    choices = ['', 'X', ':checkered_flag:', ':cat:']
    
    return np.select(conditions, choices).reshape(shape)

def _format_command_str(command:str) -> str:
    '''
    Takes a command and turn it into an understandable string.
    Conversion table:
        'move' -> '一歩進む'
        'turn' -> '右を向く'
        'if wall' -> 'IF 目の前が壁['
        'else' -> ']ELSE['
        'endif' -> ']'
    '''
    match command:
        case 'move':
            return '一歩進む'
        case 'turn':
            return '右を向く'
        case 'if wall':
            return 'IF 目の前が壁['
        case 'else':
            return ']ELSE['
        case 'endif':
            return ']'

def format_commands(commands:list[str]) -> str:
    '''
    Takes a list of commands and turn it to a string that is understandable for users.
    '''
    return '\n'.join(_format_command_str(command) for command in commands)

def rerun():
    st.session_state.board, st.session_state.start_pos, st.session_state.flag_positions = core.generate_map(**st.session_state.args)
    st.session_state.commands = list()
    st.session_state.executer = None
    return
