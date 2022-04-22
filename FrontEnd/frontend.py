import pygame

from .constants import WIDTH, HEIGHT
from .board import Board

from Chess.chess_engine import ChessEngine

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
                board.selected_piece = mouse_square
                pass

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit