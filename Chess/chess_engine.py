from .move import Move
from .constants import *


class ChessEngine:
    """
    Class for playing a game of Chess
    """

    def __init__(self):
        """
        The init method keeps track of board, movements, and logs
        """

        # keeps track of player turn, move log, piece capture, and board notation
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_turn = True
        self.move_log = []  # stores Move objects
        self.chess_notation = []  # stores chess notation of the start and end square of the move
        self.pieces_captured = []  # store pieces that have been captured
        self.legible_move_list = []  # stores full move information string for printing on the UI

        # king locations
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

        self.enpassant_coords = ()  # used to save the enpassant

        # keep track of check mate and stalemate
        self.checkmate = False
        self.stalemate = False

    def make_move(self, move: Move):
        """
        Accepts a Move object to update the board and move log
        Does not validate the move!!
        """

        # update self.board by moving the piece to the coordinates
        self.board[move.start_row][move.start_col] = None
        self.board[move.end_row][move.end_col] = move.get_piece_moved()

        # update the lists pertaining to move history
        self.move_log.append(move)
        self.chess_notation.append(move.get_chess_notation())
        self.legible_move_list.append(move.get_move_legible())
        if move.get_piece_captured():
            self.pieces_captured.append(move.piece_captured)

        self.change_turn()

        # update king location
        if move.piece_moved == 'wK':
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_loc = (move.end_row, move.end_col)

        # pawn promotion
        if move.pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        # if an enpassant moved was made, then the square behind needs to be set to false
        if move.enpassant_move:
            self.board[move.start_row][move.end_col] = None

        # if current piece moved two places then save enpassant square to capture else set to empty
        if (move.piece_moved == 'wP' or move.piece_moved == 'bP') and abs(move.start_row - move.end_row) == 2:
            self.enpassant_coords = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant_coords = ()

        if move.castling_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = move.piece_moved[0] + 'R'
                self.board[move.end_row][move.end_col + 1] = None
            else:
                self.board[move.end_row][move.end_col + 1] = move.piece_moved[0] + 'R'
                self.board[move.end_row][move.end_col - 2] = None

    def undo_move(self):
        """
        Undoes the last move
        """

        # make sure that there is actually move to undo or error is thrown
        if len(self.move_log) > 0:
            # get the Move object being undone and remove the last entry from all the logs
            undone_move = self.move_log.pop()
            self.chess_notation.pop()
            self.legible_move_list.pop()
            if undone_move.piece_captured is not None:
                self.pieces_captured.pop()

            # undo the piece locations
            self.board[undone_move.start_row][undone_move.start_col] = undone_move.piece_moved
            self.board[undone_move.end_row][undone_move.end_col] = undone_move.piece_captured

            # change the turn
            self.change_turn()

            # update king location
            if undone_move.piece_moved == 'wK':
                self.white_king_loc = (undone_move.start_row, undone_move.start_col)
            elif undone_move.piece_moved == 'bK':
                self.black_king_loc = (undone_move.start_row, undone_move.start_col)

            # if a move that was undone was an enpassant then reset the values of the square
            if undone_move.enpassant_move:
                self.board[undone_move.end_row][undone_move.end_col] = None
                self.board[undone_move.start_row][undone_move.end_col] = undone_move.piece_captured
                self.enpassant_coords = (undone_move.end_row, undone_move.end_col)

            # undo a two pawn on advance
            if (undone_move.piece_moved == 'wP' or undone_move.piece_moved == 'bP') and \
                    (abs(undone_move.start_row - undone_move.end_row) == 2):
                self.enpassant_coords = ()

            # if castle move undo the move
            if undone_move.castling_move:
                if undone_move.end_col - undone_move.start_col == 2:
                    self.board[undone_move.end_row][undone_move.end_col + 1] = self.board[undone_move.end_row][
                        undone_move.end_col - 1]
                    self.board[undone_move.end_row][undone_move.end_col - 1] = None
                else:
                    self.board[undone_move.end_row][undone_move.end_col - 2] = self.board[undone_move.end_row][
                        undone_move.end_col + 1]
                    self.board[undone_move.end_row][undone_move.end_col + 1] = None

    def valid_moves(self):
        """
        moves considering if a check or checkmate can happen, so this function will filter out those moves and not allow
        for the player to make those
        """

        # save the current enpassant to restore it later
        temp_enpassant = self.enpassant_coords

        # generate all possible moves for the current color
        moves = self.all_moves()

        # castling moves need to be made outside all moves
        if self.white_turn:
            self.castling_moves(self.white_king_loc[0], self.white_king_loc[1], WHITE, moves)
        else:
            self.castling_moves(self.black_king_loc[0], self.black_king_loc[1], BLACK, moves)

        # check if any of the moves would put the turn player in check (invalid move)
        for i in range(len(moves) - 1, -1, -1):
            sim_move = moves[i]
            self.make_move(sim_move)
            self.change_turn()

            # if king is attacked then not a valid move
            if self.is_in_check(sim_move.get_piece_moved()[0]):
                moves.remove(moves[i])

            self.change_turn()
            self.undo_move()

        # if there are no moves left then it is either checkmate or stalemate
        if len(moves) == 0:
            # if its in check, then it is also checkmate
            if self.is_in_check(WHITE) or self.is_in_check(BLACK):
                self.checkmate = True
            # else its stalemate
            else:
                self.stalemate = True

        # restore the current enpassant
        self.enpassant_coords = temp_enpassant

        return moves

    def is_in_check(self, color, castling_row=0, castling_col=0, castling=False) -> bool:
        """
        determines if the enemy can attack the current players king
        """
        row = castling_row
        col = castling_col

        # determine which king to determine if it is in check
        if not castling:
            if color == WHITE:
                row = self.white_king_loc[0]
                col = self.white_king_loc[1]
            else:
                row = self.black_king_loc[0]
                col = self.black_king_loc[1]

        # switch to opponent to see the opponent's moves
        self.change_turn()
        opponent_moves = self.all_moves()

        # change the turn back
        self.change_turn()

        # loop through the opponent's moves
        for move in opponent_moves:
            # if the row and col is the matched what is passed to function that king is attacked
            if move.end_row == row and move.end_col == col:
                return True

        return False

    def all_moves(self):
        """
        Returns a list of all moves to empty space or to capture enemy piece for piece of the turn player
        Does not consider if the move puts the turn player in check/checkmate
        """

        all_moves = []  # list of Move objects

        # check each board location
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                cur_piece = self.board[row][col]

                # there is a piece at the board location (is not None)
                if cur_piece:
                    cur_piece_color = cur_piece[0]

                    # if the piece is the same color of the turn player
                    if (cur_piece_color == WHITE and self.white_turn) or (
                            cur_piece_color == BLACK and not self.white_turn):
                        # get all the piece's possible moves according to what piece it is and position
                        if cur_piece[1] in 'P':
                            self.pawn_moves(row, col, cur_piece_color, all_moves)
                        elif cur_piece[1] in 'RBQ':
                            self.moves_rbq(row, col, cur_piece[1], cur_piece_color, all_moves)
                        elif cur_piece[1] in 'NK':
                            self.moves_nk(row, col, cur_piece[1], cur_piece_color, all_moves)

        return all_moves

    def pawn_moves(self, row, col, color, moves_list):
        """
        Creates a Move object for every possible move for a pawn at the location and adds it to the list
        """
        # white pawn (correct turn player already determined in all_moves)
        if color == WHITE:
            # if first position up is empty then add the Move object for the move
            if self.is_empty_square(row - 1, col):
                moves_list.append(Move((row, col), (row - 1, col), self.board))

                # it is in starting position then add the two move jump to the list
                if row == 6 and self.is_empty_square(row - 2, col):
                    moves_list.append(Move((row, col), (row - 2, col), self.board))

            # check if pawn has a piece to capture diagonally up
            if self.is_enemy_piece(row - 1, col - 1, color):
                moves_list.append(Move((row, col), (row - 1, col - 1), self.board))
            if self.is_enemy_piece(row - 1, col + 1, color):
                moves_list.append(Move((row, col), (row - 1, col + 1), self.board))

            # enpassant move
            if self.is_empty_square(row - 1, col - 1):
                if self.enpassant_coords == (row - 1, col - 1):
                    moves_list.append(Move((row, col), (row - 1, col - 1), self.board, enpassant=True))
            if self.is_empty_square(row - 1, col + 1):
                if self.enpassant_coords == (row - 1, col + 1):
                    moves_list.append(Move((row, col), (row - 1, col + 1), self.board, enpassant=True))

        # black pawn
        elif color == BLACK:
            # if first position down is empty then add the Move object for the move
            if self.is_empty_square(row + 1, col):
                moves_list.append(Move((row, col), (row + 1, col), self.board))

                # it is in starting position then add the two move jump to the list
                if row == 1 and self.is_empty_square(row + 2, col):
                    moves_list.append(Move((row, col), (row + 2, col), self.board))

            # check if pawn has a piece to capture diagonally down
            if self.is_enemy_piece(row + 1, col - 1, color):
                moves_list.append(Move((row, col), (row + 1, col - 1), self.board))
            if self.is_enemy_piece(row + 1, col + 1, color):
                moves_list.append(Move((row, col), (row + 1, col + 1), self.board))

            # make enpassant move
            if self.is_empty_square(row + 1, col - 1):
                if self.enpassant_coords == (row + 1, col - 1):
                    moves_list.append(Move((row, col), (row + 1, col - 1), self.board, enpassant=True))
            if self.is_empty_square(row + 1, col + 1):
                if self.enpassant_coords == (row + 1, col + 1):
                    moves_list.append(Move((row, col), (row + 1, col + 1), self.board, enpassant=True))

    def moves_rbq(self, row, col, piece, color, moves_list):
        """
        This function handles all the Queen, Bishop, and Rook moves
        """

        # bishops can move diagonally all directions and as many spaces as possible
        # rook can move cross directions and as many spaces as possible
        # queen can move as a bishop and rook
        move_directions = {'Q': [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]],
                           'B': [[1, 1], [1, -1], [-1, -1], [-1, 1]],
                           'R': [[0, 1], [0, -1], [-1, 0], [1, 0]]}

        # for direction of movement for the piece
        for mov_dir in move_directions[piece]:
            # location of potential move in the direction of mov_dir
            cur_row = row + mov_dir[0]
            cur_col = col + mov_dir[1]

            # add empty spaces in that direction (is_empty_square checks for valid row/col)
            while self.is_empty_square(cur_row, cur_col):
                moves_list.append(Move((row, col), (cur_row, cur_col), self.board))
                cur_row += mov_dir[0]
                cur_col += mov_dir[1]

            # check if one more space has an enemy piece (is_enemy_piece checks for valid row/col)
            if self.is_enemy_piece(cur_row, cur_col, color):
                moves_list.append(Move((row, col), (cur_row, cur_col), self.board))

    def moves_nk(self, row, col, piece, color, moves_list):
        """
        this function handles king and knight moves
        """
        # both knight and king can move 8 possible directions one time
        move_directions = {"N": [[-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]],
                           "K": [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]}

        for mov_dir in move_directions[piece]:
            # location of potential move in the direction of mov_dir
            cur_row = row + mov_dir[0]
            cur_col = col + mov_dir[1]

            # if the potential move is empty or has an enemy piece
            if self.is_empty_square(cur_row, cur_col) or self.is_enemy_piece(cur_row, cur_col, color):
                moves_list.append(Move((row, col), (cur_row, cur_col), self.board))

    def castling_moves(self, row, col, color, moves_list):
        """
        determines what the castling moves can be made if castling rights are eligible
        """

        # if king is in check then return false
        if self.is_in_check(color, castling_row=row, castling_col=col, castling=True):
            return

        # gather the rights for each rook and king
        castle_rights = self.get_castling_rights()

        # gather the castling moves that are possible for the king
        if (color == WHITE and castle_rights[0]) or (color == BLACK and castle_rights[1]):
            self.king_side_castle(row, col, color, moves_list)

        # gather the castling moves that are possible for the queen
        if (color == WHITE and castle_rights[2]) or (color == BLACK and castle_rights[3]):
            self.queen_side_castle(row, col, color, moves_list)

    def king_side_castle(self, row, col, color, moves_list):
        """
        returns the moves for castling of king side
        """
        if self.is_empty_square(row, col + 1) and self.is_empty_square(row, col + 2):
            if not self.is_in_check(color, castling_row=row, castling_col=col+1, castling=True) \
                    and not self.is_in_check(color, castling_row=row, castling_col=col+2, castling=True):
                moves_list.append(Move((row, col), (row, col + 2), self.board, castle=True))

    def queen_side_castle(self, row, col, color, moves_list):
        """
        returns the moves for castling of queen side
        """
        if self.is_empty_square(row, col-1) and self.is_empty_square(row, col-2) and self.is_empty_square(row, col-3):
            if not self.is_in_check(color, castling_row=row, castling_col=col-1, castling=True) \
                    and not self.is_in_check(color, castling_row=row, castling_col=col-2, castling=True):
                moves_list.append(Move((row, col), (row, col - 2), self.board, castle=True))

    def get_castling_rights(self):
        """
        The method gathers rights of the castling capabilities for white king and queens side and black king and
        queen side. It then returns True or False for each of the four eligibility.
        """

        # set all castling rights to True
        wks, bks, wqs, bqs = True, True, True, True
        for i in range(len(self.move_log)):

            # if king moved, then both white king side and black side are False
            if self.move_log[i].piece_moved == 'wK':
                wks, wqs = False, False

            # same as above but for black
            if self.move_log[i].piece_moved == 'bK':
                bks, bqs = False, False

            # check if either white rook moved and set the rights accordingly
            if self.move_log[i].piece_moved == 'wR':
                if self.move_log[i].start_row == 7 and self.move_log[i].start_col == 0:
                    wqs = False
                elif self.move_log[i].start_row == 7 and self.move_log[i].start_col == 7:
                    wks = False

            # check if either black rook moved and set the rights accordingly
            if self.move_log[i].piece_moved == 'bR':
                if self.move_log[i].start_row == 0 and self.move_log[i].start_col == 0:
                    wqs = False
                elif self.move_log[i].start_row == 0 and self.move_log[i].start_col == 7:
                    wks = False

        # help
        return [wks, bks, wqs, bqs]

    def get_board(self):
        """
        returns the board
        """
        return self.board

    def is_enemy_piece(self, row, col, player_color):
        """
        Returns a boolean for whether a space contains an enemy piece
        """
        # check for valid space, piece at the space, and non-matching color
        if is_in_bounds(row, col) and self.board[row][col] is not None and self.board[row][col][0] != player_color:
            return True
        return False

    def is_empty_square(self, row, col):
        """
        Returns a boolean for whether a space is empty
        """
        # check for valid space, None at the space
        if is_in_bounds(row, col) and self.board[row][col] is None:
            return True
        return False

    def change_turn(self):
        """
        Changes the turn player
        not self.white_turn means self.white_turn is False, => black move
        """
        self.white_turn = not self.white_turn

    def get_square(self, row, column):
        """
        Returns the piece located at the square. Return None is no piece is there
        """
        return self.board[row][column]
