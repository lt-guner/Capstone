import pygame

from constants import *
from pieces import *

PIECE_OFFSET = (SQUARE_SIZE - PIECE_IMG_SIZE)/2
class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0

    def draw_squares(self, win):
        win.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win, layout):
        for row in range(ROWS):
            for col in range(COLS):
                piece = layout[row][col]
                if piece != None:
                    win.blit(pieceImages[piece], (col * SQUARE_SIZE + PIECE_OFFSET, row * SQUARE_SIZE + PIECE_OFFSET))

    def get_mouse_square(self):
        mouse_coords = pygame.mouse.get_pos()
        col = mouse_coords[0]//SQUARE_SIZE
        row = mouse_coords[1]//SQUARE_SIZE
        return (row,col)

    def draw_selected(self, win):
        if self.selected_piece:
            row, col = self.selected_piece
            pygame.draw.rect(win, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
