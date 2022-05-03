import pygame

from .constants import *
from .pieces import *

PIECE_OFFSET = (SQUARE_SIZE - PIECE_IMG_SIZE)/2
class Board:
    # Citation for code to render the board: Tech With Tim, U.S., Python/Pygame Checkers Tutorial (Part 1) - Drawing the Board: (2020).
    # Accessed: April 10, 2022. [Online Video]. Available: https://www.youtube.com/watch?v=vnd3RfeG3NM
    def __init__(self, player_color):
        self.piece_chosen = None
        self.board = []
        self.black_left = self.white_left = 12
        self.black_pc = self.white_pc = 0
        self.player_color = player_color

    # Flips the board for the black player
    def virt_coords(self, row, col):
        if self.player_color == WHITE:
            return row, col
        else:
            return ROWS-row-1, COLS-col-1

    def draw_squares(self, win):
    # Citation for code to render the board: Tech With Tim, U.S., Python/Pygame Checkers Tutorial (Part 1) - Drawing the Board: (2020).
    # Accessed: April 10, 2022. [Online Video]. Available: https://www.youtube.com/watch?v=vnd3RfeG3NM
        win.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win, layout):
        for row in range(ROWS):
            for col in range(COLS):
                piece = layout[row][col]
                if piece != None:
                    # Transforming the coordinates for player view
                    vrow, vcol = self.virt_coords(row, col)
                    win.blit(pieceImages[piece], (vcol * SQUARE_SIZE + PIECE_OFFSET, vrow * SQUARE_SIZE + PIECE_OFFSET))

    def get_mouse_square(self):
        mouse_coords = pygame.mouse.get_pos()
        # Transforming the coordinates for player view
        vrow, vcol = self.virt_coords(mouse_coords[1]//SQUARE_SIZE, mouse_coords[0]//SQUARE_SIZE)
        return (vrow,vcol)

    def draw_selected(self, win):
        if self.piece_chosen:
            # Transforming the coordinates for player view
            vrow, vcol = self.virt_coords(*self.piece_chosen)
            pygame.draw.rect(win, GREEN, (vcol * SQUARE_SIZE, vrow * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
