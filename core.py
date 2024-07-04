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

    indices = np.where(board == 0)
    flag_positions = [rng.choice(indices[0], size = flags), rng.choice(indices[1], size = flags)]

    board[flag_positions[0], flag_positions[1]] = FLAG

    starting_position = (lines_x[0], len(board[:,0]) - 1)

    return board, starting_position

def recurse(func):
    '''
    Recursively execute commands until either all flags are captured or the player drops out of the board.
    '''
  
    @wraps(func)
    def _wrapper(commands, board, start):
        pos:tuple = None
        count = 0
        executor = func(commands, board, start)

        while len(np.where(board == 0.5)[0]) != 0:
            try:
                pos, count = executor.__next__()[0]
                yield pos
            except IndexError:
                return f'{count}枚の旗を見つけました...惜しい...'
            except Exception as e:
                return f'Unknown error:{e}'
        return 'すべての旗を見つけました！'

    return _wrapper

@recurse
def execute(commands:list[str], board:np.ndarray, start:tuple):
    '''
    Recieves commands and a board and execute the commands.
    Returns the count of how many flags did the player succeed to get.
    '''

    # To count how many flags did the program achieve
    count = 0
    # To record which way is the player facing to
    direction = 90 # 0, 90, 180, 270
    # To record where the player is
    position = start
    # To record if block
    ignore = False

    # Constants
    PLAYER = 0.25
    FLAG = 0.5

    for command in commands:
        yield position, count # For tracking where have the programm reached so far

        # Refresh count
        if board[position[0], position[1]] == FLAG:
                            count += 1
                            board[position[0], position[1]] = 0

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
                    case 0:
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0] + 1, position[1]] = PLAYER
                        # Refresh position
                        position = (position[0] + 1, position[1])

                    case 90:
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0], position[1] - 1] = PLAYER
                        # Refresh position
                        position = (position[0], position[1] - 1)

                    case 180:
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0] - 1, position[1]] = PLAYER
                        # Refresh position
                        position = (position[0] - 1, position[1])

                    case 270:
                        # Move player
                        board[position[0], position[1]] = 0
                        board[position[0], position[1] + 1] = PLAYER
                        # Refresh position
                        position = (position[0], position[1] + 1)

            case 'turn':
                direction = (direction + 90) % 360

            case 'if wall':
                pos = position
                match direction:
                    case 0:
                        pos = (pos[0] + 1, pos[1])
                    case 90:
                        pos = (pos[0], pos[1] + 1)
                    case 180:
                        pos = (pos[0] - 1, pos[1])
                    case 270:
                        pos = (pos[0], pos[1] - 1)
                if board[pos[0], pos[1]] == 1:
                    ignore = True

            case 'endif':
                continue # This endif command should be a part of the if block that was executed successfully

            case 'else':
                continue # This else command should be a part of the if block that was executed successfully

            case _:
                raise ValueError('Invalid command')
