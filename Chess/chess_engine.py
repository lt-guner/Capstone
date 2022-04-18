from move import Move


class ChessEngine:
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
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        # keeps track of player turn, move log, piece capture, and board notation
        self.white_move = True
        self.move_log = []
        self.chess_notation = []
        self.pieces_captured = []
        self.legible_move_list = []

        # king locations
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

        # keep track of check mate and stalemate
        self.checkmate = False
        self.stalemate = False

    def make_move(self, move):
        """
        moves the piece based on move variable (not for castling, en passant, and pawn promotion)
        """

        # make the square blank the piece was moved from and update the piece at the selected square
        self.board[move.start_row][move.start_col] = "--"

        # update the piece to the ending location
        self.board[move.end_row][move.end_col] = move.piece_moved

        # append move to object to move log
        self.move_log.append(move)

        # append the chess notation to the chess notation log
        self.chess_notation.append(move.get_chess_notation())

        # append the legible moves to move log
        self.legible_move_list.append(move.get_move_legible())

        # add captured piece to list if a piece was captured
        if move.piece_captured != '--':
            self.pieces_captured.append(move.piece_captured)

        # set the which turn it is next
        if self.white_move:
            self.white_move = False
        else:
            self.white_move = True

        # update king location
        if move.piece_moved == 'wK':
            self.white_king_loc = (move.end_row, move.end_col)
        if move.piece_moved == 'bK':
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        """
        undoes the last undone_move
        """

        # make sure that there is actually a undone_move or error is thrown
        if len(self.move_log) == 0:
            return

        # pop the undone_move and put the undone_move the piece back to start position and change the end position back
        # to piece captured which is either a black or enemy piece
        # pop all the other undone_move logs beside move_log
        undone_move = self.move_log.pop()
        self.legible_move_list.pop()
        self.chess_notation.pop()
        self.board[undone_move.start_row][undone_move.start_col] = undone_move.piece_moved
        self.board[undone_move.end_row][undone_move.end_col] = undone_move.piece_captured
        if undone_move.piece_captured != '--':
            self.pieces_captured.pop()

        # set the which turn it is next
        if self.white_move:
            self.white_move = False
        else:
            self.white_move = True

        # update king location
        if undone_move.piece_moved == 'wK':
            self.white_king_loc = (undone_move.start_row, undone_move.start_col)
        if undone_move.piece_moved == 'bK':
            self.black_king_loc = (undone_move.start_row, undone_move.start_col)

    def valid_moves(self):
        """
        moves considering if a check or checkmate can happen, so this function will filter out those moves and not allow
        for the player to make those
        """

        # generate all possible moves for the current color
        moves = self.all_moves()

        # for each move, make the move for the current color
        # best to go backwards when removing from a list for indexing reasons
        # https://thispointer.com/python-different-ways-to-iterate-over-a-list-in-reverse-order/
        for x in range(len(moves) - 1, -1, -1):
            self.make_move(moves[x])

            # make_moves switches turns, so we need to switch it back to current color
            self.white_move = not self.white_move

            # if king is attacked then its not a valid move
            if self.is_in_check():
                moves.remove(moves[x])

            # switch players turn to the opponent so the opponent can make the move in the next turn
            # and to cancel out the original moves made and swapped
            self.white_move = not self.white_move
            self.undo_move()

        # if there are no moves left then it is either checkmate or stalemate
        if len(moves) == 0:
            # if its in check, then it is also checkmate
            if self.is_in_check():
                self.checkmate = True
            # else its stalemate
            else:
                self.stalemate = False

        return moves

    def is_in_check(self):
        """
        determines if the enemy can attack the current players king
        """

        row = 0
        col = 0

        if self.white_move:
            row = self.white_king_loc[0]
            col = self.white_king_loc[1]
        else:
            row = self.black_king_loc[0]
            col = self.black_king_loc[1]

        # switch to opponent to see the opponent's moves
        self.white_move = not self.white_move
        opponent_moves = self.all_moves()

        # make sure that the turn is switched back to the current player, we are not modifying the turn
        self.white_move = not self.white_move

        # loop through the opponent's moves
        for move in opponent_moves:
            # if the row and col is the matched what is passed to function that king is attacked
            if move.end_row == row and move.end_col == col:
                return True

        return False

    def all_moves(self):
        """
        All possible moves available regardless if it will cause the player check or checkmate
        """
        moves = []

        # double loop through board to check each board location like in Kuba game from c162
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # this pulls the following color of the piece because it's the 0th index of the string
                # don't use == for True or False, just use "not" for false checking for linting errors
                current_piece_color = self.board[row][col][0]
                if (current_piece_color == "w" and self.white_move) or (
                        current_piece_color == 'b' and not self.white_move):
                    # now generate the moves for each piece which is the second char in each string
                    # if pawn
                    if self.board[row][col][1] == "P":
                        # call the function to the pawn moves
                        self.pawn_moves(row, col, moves)
                    # if castle
                    elif self.board[row][col][1] == "R" or self.board[row][col][1] == "B" or \
                            self.board[row][col][1] == "Q":
                        # call the function to the castle moves
                        self.moves_rbq(row, col, self.board[row][col][1], moves)
                    # if knight or king
                    elif self.board[row][col][1] == "N" or self.board[row][col][1] == "K":
                        # call the function to get knight moves
                        self.moves_nk(row, col, self.board[row][col][1], moves)

        return moves

    def pawn_moves(self, row, col, moves):
        """
        Gets all the pawn moves for the pawn at location row and col and adds to list
        """

        # check if whites turn
        if self.white_move and self.board[row][col][0] == 'w':
            # if first position up is empty then add to move list with Moves Class
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                # it is in starting position then add the two move jump to the list
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            # captures left diagonal and right diagonal
            # check left diagonal has a black piece and is not out of bounds
            if col - 1 >= 0:
                # diagonal left check is black and then capture
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            # now captures to the right
            if col + 1 <= len(self.board[row]) - 1:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        # blacks turn which is reverse of white
        elif not self.white_move and self.board[row][col][0] == 'b':
            # if first position up is empty then add to move list with Moves Class
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                # it is in starting position then add the two move jump to the list
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            # captures left diagonal and right diagonal
            # check left diagonal has a black piece and is not out of bounds
            if col - 1 >= 0:
                # diagonal left check is black and then capture
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            # now captures to the right
            if col + 1 <= len(self.board[row]) - 1:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def moves_rbq(self, row, col, piece, moves):
        """
        This function handles all the Queen, Bishop, and Rook moves
        """

        # bishops can move diagonal all directions and as many spaces as possible
        # rook can move cross directions and as many spaces as possible
        # queen can move as a bishop and rook
        move_directions = {'Q': [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]],
                           'B': [[1, 1], [1, -1], [-1, -1], [-1, 1]],
                           'R': [[0, 1], [0, -1], [-1, 0], [1, 0]]}

        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # loop through the move list based on if its a queen, bishop, or rook
        for x in range(len(move_directions[piece])):
            # the pieces can move seven spots in all directeions
            for y in range(1, len(self.board[row])):
                # we are calculating the current directions based on move_directions
                cur_row = row + move_directions[piece][x][0] * y
                cur_col = col + move_directions[piece][x][1] * y
                # to proceed makes sure move is in bounds
                if (cur_row >= 0 and cur_row < len(self.board[row])) and \
                        (cur_col >= 0 and cur_col < len(self.board[row])):
                    # check to see if the current square is empty
                    if self.board[cur_row][cur_col] == "--":
                        moves.append(Move((row, col), (cur_row, cur_col), self.board))
                    # check if it is an enemy piece that can be captured
                    elif enemy_color == self.board[cur_row][cur_col][0]:
                        moves.append(Move((row, col), (cur_row, cur_col), self.board))
                        break
                    else:
                        # we hit an enemy piece
                        break
                else:
                    # we hit the end of the board so break
                    break

    def moves_nk(self, row, col, piece, moves):
        """
        this function handles king and knight moves
        """

        # both knight and king can move 8 possible directions one time
        move_directions = {"N": [[-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]],
                           "K": [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]}

        # the color of the opponent
        enemy_color = 'w'
        if self.white_move:
            enemy_color = 'b'

        # loop through the eight positions
        for x in range(len(move_directions[piece])):
            # get the square location using the move_directions
            cur_row = row + move_directions[piece][x][0]
            cur_col = col + move_directions[piece][x][1]
            # to proceed makes sure move is in bounds
            if (cur_row >= 0 and cur_row < len(self.board[row])) and (cur_col >= 0 and cur_col < len(self.board[row])):
                # move to location if it is empty or has an enemy piece
                if self.board[cur_row][cur_col] == "--" or enemy_color == self.board[cur_row][cur_col][0]:
                    moves.append(Move((row, col), (cur_row, cur_col), self.board))
