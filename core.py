import numpy as np
from functools import wraps

def generate_map(size:tuple[int, int], complexity_x:int = 1, complexity_y:int = 1, flags:int = 1):
    '''
    Takes the size of the board, and how many walkable lines to create, and the number of the targets.
    The size of the board will be shrinked by one for each axis.
    '''

    FLAG = 0.5
    # There should be at least one block of wall on the outer lim
    size = (size[0] - 1, size[1] - 1)
    # Check validity of the arguments
    if size[0] < 1 or size[1] < 1:
        raise ValueError('Board too small')
    if complexity_x < 1 or complexity_y < 1:
        raise ValueError('There should be at least one walkable line for both x and y')

    # Board. 1 represents a wall.
    board = np.ones(size)
    rng = np.random.default_rng()
    lines_x = rng.integers(0, size[0], size=complexity_x)
    lines_y = rng.integers(0, size[1], size=complexity_y)
    # Create walkable lines
    board[:, lines_x] = 0
    board[lines_y, :] = 0

    flag_positions = rng.choice(np.argwhere(board == 0), size = flags)

    for flag_y, flag_x in flag_positions:
        board[flag_y, flag_x] = FLAG

    starting_position = (len(board[:,0]) - 1, lines_x[0])

    board[starting_position[0], starting_position[1]] = 0.25

    return board, starting_position, flag_positions

def recurse(func):
    '''
    Takes the execute function below and recusively calls it until either all flags are captured
    or the player falls off the board.
    '''
    @wraps(func)
    def _wrapper(commands, board, start):
        flag_count = 1
        direction = 90
        executor = func(commands, board, start, direction)
        while True:
            try:
                pos, count, direction = executor.__next__()
                if count == 0:
                    raise IndexError() # Ends the execution process
                else:
                    yield pos, count
            except StopIteration:
                executor = func(commands, board, pos, direction)
                continue

    return _wrapper

@recurse
def execute(commands:list[str], board:np.ndarray, start:tuple, start_direction:int = 90):
    '''
    Recieves commands and a board and execute the commands.
    Returns the count of how many flags did the player succeed to get.
    '''

    # To count how many flags did the program achieve
    count = len(np.where(board == 0.5)[0])
    # To record which way is the player facing to
    direction = start_direction # 0, 90, 180, 270
    # To record where the player is
    position = start
    # To record if block
    ignore = False

    # Constants
    PLAYER = 0.25
    FLAG = 0.5

    for command in commands:

        # Refresh count
        if board[position[0], position[1]] == FLAG:
            count -= 1
            board[position[0], position[1]] = 0.25

        if ignore:
            if command == 'endif':
                ignore = False
                continue
            elif command == 'else':
                pass # Should execute this part
            else:
                continue

        match command:
            case 'move':
                match direction:
                    case 0 if (board[position[0], position[1]] != 0): # Check if the player is in an invalid area
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0], position[1] + 1] = PLAYER
                        # Refresh position
                        position = (position[0], position[1] + 1)
                
                    case 90 if (board[position[0], position[1]] != 1):
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0] - 1, position[1]] = PLAYER
                        # Refresh position
                        position = (position[0] - 1, position[1])

                    case 180 if (board[position[0], position[1]] != 1):
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0], position[1] - 1] = PLAYER
                        # Refresh position
                        position = (position[0], position[1] - 1)

                    case 270 if (board[position[0], position[1]] != 1):
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0] + 1, position[1]] = PLAYER
                        # Refresh position
                        position = (position[0] + 1, position[1])

                    case _: # Blocked by the if guard statement, which means that the position is invalid
                        raise IndexError() # Ends the execution process

            case 'turn':
                direction = (direction - 90) % 360

            case 'lturn':
                direction = (direction + 90) % 360

            case 'if wall':
                pos = position
                match direction:
                    case 0:
                        pos = (pos[0], pos[1] + 1)
                    case 90:
                        pos = (pos[0] - 1, pos[1])
                    case 180:
                        pos = (pos[0], pos[1] - 1)
                    case 270:
                        pos = (pos[0] + 1, pos[1])
                if board[pos[0], pos[1]] == 1:
                    ignore = True

            case 'endif':
                continue # This endif command should be a part of the if block that was executed successfully

            case 'else':
                continue # This else command should be a part of the if block that was executed successfully

            case _:
                raise ValueError('Invalid command')


        yield position, count, direction # For tracking where have the programm reached so far
