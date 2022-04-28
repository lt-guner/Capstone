import pygame

from .constants import WIDTH, HEIGHT
from .board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move

engine = ChessEngine()

FPS = 60

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Chess')

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    while run:
        clock.tick(FPS)

        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.selected_piece:
                    move = Move(board.selected_piece, mouse_square, engine.board)
                    # make a move if it is a valid move and set move_made to true
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            engine.make_move(valid_moves[i])
                            move_made = True
                    board.selected_piece = None
                else:
                    row, col = mouse_square
                    if not engine.is_empty_square(row, col):
                        board.selected_piece = mouse_square
        # get the next set of valid moves and reset move_made
        if move_made:
            valid_moves = engine.valid_moves()
            move_made = False

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit