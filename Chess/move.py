class Move:
    """
    The init takes the first clicked square and second clicked square and stores the starting and ending coords.
    It then stores the piece that moved and piece that was captured based on that starting and ending coords.
    """

    def __init__(self, startSq, endSq, board):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # creates a unique id like a hash function
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        self.pieces = {'wP': "White Pawn", 'wR': 'White Rook', 'wN': 'White Knight', 'wB': 'White Bishop',
                       'wQ': 'White Queen', 'wK': 'White King', 'bP': "Black Pawn", 'bR': 'Black Rook',
                       'bN': 'Black Knight', 'bB': 'Black Bishop', 'bQ': 'Black Queen', 'bK': 'Black King'}
        self.columns_chess = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        self.rows_chess = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}

    def __eq__(self, other):
        """
        overriding the equal's method to the method
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """
        Returns the chess notation of the move like E4 E5 which is moving a piece from E4 to E5
        """

        return str(self.columns_chess[self.start_col]) + str(self.rows_chess[self.start_row]) + " " + \
            str(self.columns_chess[self.end_col]) + str(self.rows_chess[self.end_row])

    def get_move_legible(self):
        """
        Returns a human legible move to be used when logging the move in the UI
        """

        if self.piece_captured == '--':
            return str(self.move_id) + ': ' + self.pieces[self.piece_moved] + ' Moves From ' + \
                   str(self.columns_chess[self.start_col]) + str(self.rows_chess[self.start_row]) + ' to ' + \
                   str(self.columns_chess[self.end_col]) + str(self.rows_chess[self.end_row])
        else:
            return str(self.move_id) + ': ' + self.pieces[self.piece_moved] + ' Moves From ' + \
                   str(self.columns_chess[self.start_col]) + str(self.rows_chess[self.start_row]) + ' to ' + \
                   str(self.columns_chess[self.end_col]) + str(self.rows_chess[self.end_row]) + ' Capturing ' + \
                   self.pieces[self.piece_captured]

    def get_piece_captured(self):
        """
        Returns the name of the captured piece
        """

        return self.pieces[self.piece_captured]