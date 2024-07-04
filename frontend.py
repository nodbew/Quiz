import numpy as np

def _no_change(x):
    return x

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
    return np.where(
        np.where(
            np.where(board == 0, '', _no_change) == 1, #(replaced walkable) == wall
            'X', 
            _no_change
        ) == 0.5, # Flags
        ':checkered_flag:',
        ':cat:' # Player
    )
