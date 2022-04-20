WHITE = 'w'
BLACK = 'b'

PIECES = {
    'wP': "White Pawn",
    'wR': 'White Rook',
    'wN': 'White Knight',
    'wB': 'White Bishop',
    'wQ': 'White Queen',
    'wK': 'White King',
    'bP': "Black Pawn",
    'bR': 'Black Rook',
    'bN': 'Black Knight',
    'bB': 'Black Bishop',
    'bQ': 'Black Queen',
    'bK': 'Black King'
}

PIECE_VALUE = {
    'Pawn': 1,
    'Knight': 3,
    'Bishop': 3,
    'Rook': 5,
    'Queen': 9,
    'King': 10
}
COL_TO_NOTATION = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
ROW_TO_NOTATION = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}


def is_in_bounds(row, col):
    """
    Returns a boolean for whether a space coordinate is on the 8x8 board
    """
    # board is 8x8, stored as 2D list with indexes 0-7
    return 0 <= row <= 7 and 0 <= col <= 7