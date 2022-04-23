import pygame

from .constants import WIDTH, HEIGHT
from .board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move

engine = ChessEngine()

FPS = 60

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Chess')

# variable to store player color (get from client upon connection)
# use player color and engine.white_turn to determine if it's the player's turn

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if user's turn:
            # (indent code below when if statement is implemented)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.selected_piece:
                    move = Move(board.selected_piece, mouse_square, engine.board, len(engine.move_log))
                    # call game engine (piece)_move() to get list of valid moves for this piece and location
                    # if move is in valid_moves_list
                        # place move into data buffer shared with client to read and send to server
                        # engine.make_move(move) --- below
                        # board.selected_piece = None --- below
                    # else nothing or deselect piece (place piece back)

                    engine.make_move(move)
                    board.selected_piece = None
                else:
                    row, col = mouse_square
                    if not engine.is_empty_square(row, col):
                        board.selected_piece = mouse_square
            # (end indent)
            # else: opponent turn:
                # if opponent move data buffer is not None:
                    # create Move object from opponent move data
                    # engine.make_move(opponent Move object)

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit