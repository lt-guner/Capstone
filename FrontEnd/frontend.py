import pygame

from .constants import *
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

    while run:
        clock.tick(FPS)

        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.selected_piece:
                    move = Move(board.selected_piece, mouse_square, engine.board)
                    engine.make_move(move)
                    board.selected_piece = None
                else:
                    row, col = mouse_square
                    if not engine.is_empty_square(row, col):
                        board.selected_piece = mouse_square

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit