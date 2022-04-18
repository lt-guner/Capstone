class ChessGame:
    """
    This class handles the game mechanics of setting up the board and handing the game mechanics.
    """

    def __init__(self):
        """
        The constructor method to create the board and keep track of moves and variables
        """

        # make the board, like how you made Kuba in 162
        # standard chess board of two-dimensional list
        # b is black w for white
        # chars after b or w represent the piece type
        # strings -- is an empty space no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # keeps track of player turn, move log, piece capture, and board notation
        self.white_move = True
        self.move_log = []
        self.captured_pieces = []
        self.pieces = {'wP': "White Pawn", 'wR': 'White Rook', 'wN': 'White Knight', 'wB': 'White Bishop',
                       'wQ': 'White Queen', 'wK': 'White King', 'bP': "Black Pawn", 'bR': 'Black Rook',
                       'bN': 'Black Knight', 'bB': 'Black Bishop', 'bQ': 'Black Queen', 'bK': 'Black King'}
        self.columns = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        self.rows = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}

    def make_move(self, move):
        """
        moves the piece based on move variable (not for castling, en passant, and pawn promotion)
        """

        # make the square blank the piece was moved from and update the piece at the selected square
        self.board[move.start_row][move.start_col] = "--"

        # if a piece was captured then append to captured list with the move id
        if self.board[move.end_row][move.end_col] != "--":
            self.captured_pieces.append(str(move.move_id) + ': ' + self.pieces[self.board[move.end_row][move.end_col]])

        # update the board with the piece that was moved
        self.board[move.end_row][move.end_col] = move.piece_moved
        # log the move for display purposes with move id and where it was moved too
        self.move_log.append(str(move.move_id) + ': ' + self.pieces[move.piece_moved] + ' to ' +
                             self.columns[move.end_col] + self.rows[move.end_row])

        # set the which turn it is next
        if self.white_move:
            self.white_move = False
        else:
            self.white_move = True

    def undo_move(self):
        """
        undoes the last move
        """

        # make sure that there is actually a move or error is thrown
        if len(self.move_log) != 0:
            # pop the move and put the move the piece back to start position and change the end position back to
            # piece captured which is either a black or enemy piece
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

        # set the which turn it is next
        if self.white_move:
            self.white_move = False
        else:
            self.white_move = True

    def check_status(self):
        """
        This function will determine if there is a check or checkmate in the game.
        """

        pass

    def get_valid_moves(self):
        """
        moves considering if a check or checkmate can happen, so this function will filter out those moves and not allow
        for the player to make those

        (in works)
        """

        # for now don't worry about checks just pass all moves
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        All possible moves available regardless if it will cause the player check or checkmate
        """
        moves = []

        # double loop through board to check each board location like in Kuba game from c162
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # this pulls the following color of the piece because it's the 0th index of the string
                # don't use == for True or False, just use "not" for false checking for linting errors
                current_piece_color = self.board[r][c][0]
                if (current_piece_color == "w" and self.white_move) or (
                        current_piece_color == 'b' and not self.white_move):
                    # now generate the moves for each piece which is the second char in each string
                    # if pawn
                    if self.board[r][c][1] == "P":
                        # call the function to the pawn moves
                        self.get_pawn_moves(r, c, moves)
                    # if castle
                    elif self.board[r][c][1] == "R":
                        # call the function to the castle moves
                        self.get_castle_moves(r, c, moves)
                    # if bishop
                    elif self.board[r][c][1] == "B":
                        # call the function to get bishop moves
                        self.get_bishop_moves(r, c, moves)
                    # if knight
                    elif self.board[r][c][1] == "N":
                        # call the function to get knight moves
                        self.get_knight_moves(r, c, moves)
                    # if queen
                    elif self.board[r][c][1] == "Q":
                        # call the function to get queen moves
                        self.get_queen_moves(r, c, moves)
                    # if King
                    elif self.board[r][c][1] == "K":
                        # call the function to get king moves
                        self.get_king_moves(r, c, moves)

        return moves

    def get_pawn_moves(self, r, c, moves):
        """
        Gets all the pawn moves for the pawn at location r and c and adds to list
        """

        # check if whites turn
        if self.white_move:
            # if first position up is empty then add to move list with Moves Class
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                # it is in starting position then add the two move jump to the list
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # captures left diagonal and right diagonal
            # check left diagonal has a black piece and is not out of bounds
            if c - 1 >= 0:
                # diagonal left check is black and then capture
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            # now captures to the right
            if c + 1 <= len(self.board[r]) - 1:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        # blacks turn which is reverse of white
        else:
            # if first position up is empty then add to move list with Moves Class
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                # it is in starting position then add the two move jump to the list
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures left diagonal and right diagonal
            # check left diagonal has a black piece and is not out of bounds
            if c - 1 >= 0:
                # diagonal left check is black and then capture
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            # now captures to the right
            if c + 1 <= len(self.board[r]) - 1:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_castle_moves(self, r, c, moves):
        """
        Gets all the castle moves for the rook at location r and c and adds to list
        """
        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # castles can move up down left and right
        # this means that it can move [0, 1], [0, -1], [-1, 0], [1, 0] until it reaches the end of the board, its
        # own piece, or captures an opponent
        move_directions = [[0, 1], [0, -1], [-1, 0], [1, 0]]

        # for loop through each direction type
        for d in range(len(move_directions)):
            # the castle can only move at move 7 times per direction
            for y in range(1, len(self.board[r])):
                # we are calculating the current directions based on move_directions
                cur_row = r + move_directions[d][0] * y
                cur_col = c + move_directions[d][1] * y
                # to proceed makes sure move is in bounds
                if (cur_row >= 0 and cur_row < len(self.board[r])) and (cur_col >= 0 and cur_col < len(self.board[r])):
                    # check to see if the current square is empty
                    if self.board[cur_row][cur_col] == "--":
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    # check if it is an enemy piece that can be captured
                    elif enemy_color == self.board[cur_row][cur_col][0]:
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    else:
                        # we hit an enemy piece
                        break
                else:
                    # we hit the end of the boar so break
                    break

    def get_bishop_moves(self, r, c, moves):
        """
        Gets all the bishop moves for the bishop at location r and c and adds to list
        """
        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # bishops can move diagonal in all directions
        # this means that it can move [1, 1], [1, -1], [-1, -1], [-1, 1] until it reaches the end of the board, its
        # own piece, or captures an opponent
        move_directions = [[1, 1], [1, -1], [-1, -1], [-1, 1]]

        # for loop through each direction type
        for d in range(len(move_directions)):
            # the bishop can only move at move 7 times per direction
            for y in range(1, len(self.board[r])):
                # we are calculating the current directions based on move_directions
                cur_row = r + move_directions[d][0] * y
                cur_col = c + move_directions[d][1] * y
                # to proceed makes sure move is in bounds
                if (cur_row >= 0 and cur_row < len(self.board[r])) and (cur_col >= 0 and cur_col < len(self.board[r])):
                    # check to see if the current square is empty
                    if self.board[cur_row][cur_col] == "--":
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    # check if it is an enemy piece that can be captured
                    elif enemy_color == self.board[cur_row][cur_col][0]:
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    else:
                        # we hit an enemy piece
                        break
                else:
                    # we hit the end of the boar so break
                    break

    def get_knight_moves(self, r, c, moves):
        """
        Gets all the bishop moves for the bishop at location r and c and adds to list
        """
        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # knights can move in L shaped direction which is 8 moves
        move_directions = [[-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]]

        # for loop through each direction type
        for d in range(len(move_directions)):
            # get the square location using the move_directions
            cur_row = r + move_directions[d][0]
            cur_col = c + move_directions[d][1]
            # to proceed makes sure move is in bounds
            if (cur_row >= 0 and cur_row < len(self.board[r])) and (cur_col >= 0 and cur_col < len(self.board[r])):
                # move to location if it is empty or has an enemy piece
                if self.board[cur_row][cur_col] == "--" or enemy_color == self.board[cur_row][cur_col][0]:
                    moves.append(Move((r, c), (cur_row, cur_col), self.board))

    def get_queen_moves(self, r, c, moves):
        """
        Gets all the queen moves for the queen at location r and c and adds to list
        """
        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # queens can move up down left and right and diagonal as far as possible
        # it is like moving a bishop and a knight
        move_directions = [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]

        # for loop through each direction type
        for d in range(len(move_directions)):
            # the castle can only move at move 7 times per direction
            for y in range(1, len(self.board[r])):
                # we are calculating the current directions based on move_directions
                cur_row = r + move_directions[d][0] * y
                cur_col = c + move_directions[d][1] * y
                # to proceed makes sure move is in bounds
                if (cur_row >= 0 and cur_row < len(self.board[r])) and (cur_col >= 0 and cur_col < len(self.board[r])):
                    # check to see if the current square is empty
                    if self.board[cur_row][cur_col] == "--":
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    # check if it is an enemy piece that can be captured
                    elif enemy_color == self.board[cur_row][cur_col][0]:
                        moves.append(Move((r, c), (cur_row, cur_col), self.board))
                    else:
                        # we hit an enemy piece
                        break
                else:
                    # we hit the end of the boar so break
                    break

    def get_king_moves(self, r, c, moves):
        """
        Gets all the queen moves for the queen at location r and c and adds to list
        """
        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # king can move up down left and right and diagonal one space
        # it is like moving a bishop and a knight but one space at a time
        move_directions = [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]

        # loop through the eight positions
        for d in range(len(move_directions)):
            # get the square location using the move_directions
            cur_row = r + move_directions[d][0]
            cur_col = c + move_directions[d][1]
            # to proceed makes sure move is in bounds
            if (cur_row >= 0 and cur_row < len(self.board[r])) and (cur_col >= 0 and cur_col < len(self.board[r])):
                # move to location if it is empty or has an enemy piece
                if self.board[cur_row][cur_col] == "--" or enemy_color == self.board[cur_row][cur_col][0]:
                    moves.append(Move((r, c), (cur_row, cur_col), self.board))


class Move:
    """
    The method is to be used to create a move object that will be used for keep track of moves made and a list of
    available moves that the current player can make. It was easier create
    """

    def __init__(self, start_square, end_square, board):
        """
        The init takes the first clicked square and second clicked square and stores the starting and ending coords.
        It then stores the piece that moved and piece that was captured based on that starting and ending coords.
        """

        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # creates a unique id like a hash function
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        overriding the equal's method to the method
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


if __name__ == "__main__":
    # start the game
    chess_match = ChessGame()

    # generate a list of all possible moves that the white can make
    all_moves = chess_match.get_all_possible_moves()

    # decide current move and make an object
    cur_move = Move((6, 0), (5, 0), chess_match.board)

    # make the move
    chess_match.make_move(cur_move)

    print(chess_match.board)

    # This would all be inisde a loop that would pull the available moves for the current turn, the player makes a move
    # as long as its in the available moves list, and board and moves / captured lists gets updated.
