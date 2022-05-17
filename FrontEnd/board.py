import pygame

from .constants import *
from .pieces import *

PIECE_OFFSET = (SQUARE_SIZE - PIECE_IMG_SIZE) / 2


class Board:
    """Creates the board as well as controls resources needed to draw the board on the screen."""

    # Citation for code to render the board: Tech With Tim, U.S., Python/Pygame Checkers Tutorial (Part 1) - 
    # Drawing the Board: (2020).
    # Accessed: April 10, 2022. [Online Video]. Available: https://www.youtube.com/watch?v=vnd3RfeG3NM
    def __init__(self, player_color):
        self.piece_chosen = None
        self.board = []
        self.black_left = self.white_left = 12
        self.black_pc = self.white_pc = 0
        self.player_color = player_color
        self.font = pygame.font.SysFont('Arial', COORD_FONT_SIZE)

    # Flips the board for the black player
    def virt_coords(self, row, col):
        """Depending on which player the board is being viewed by, the direction of the board must be turned 
           appropriately. This function transfroms the board coordinates into a virtual coordinate for drawing the 
           correct orientation."""
        if self.player_color == WHITE:
            return row, col
        else:
            return ROWS - row - 1, COLS - col - 1

    def draw_squares(self, win):
        """Draws squares on the board"""
        # Citation for code to render the board: Tech With Tim, U.S., Python/Pygame Checkers Tutorial (Part 1) - Drawing 
        # the Board: (2020).
        # Accessed: April 10, 2022. [Online Video]. Available: https://www.youtube.com/watch?v=vnd3RfeG3NM
        win.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_coords(self, win):
        """Draws the coordinates labels on the board. These are flipped depending on which player is viewing 
           the board."""
        # Determine Coord order
        if self.player_color == WHITE:
            nums, lets = range(8, 0, -1), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        else:
            nums, lets = range(1, 9), ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

        # Draw Numbers on the left
        for i, n in enumerate(nums):
            if (i % 2):
                n_text = self.font.render(str(n), True, LIGHT_BROWN)
            else:
                n_text = self.font.render(str(n), True, DARK_BROWN)
            win.blit(n_text, (0, i * SQUARE_SIZE))

        # Draw Letters on the bottom
        for i, n in enumerate(lets):
            if (i % 2):
                n_text = self.font.render(str(n), True, DARK_BROWN)
            else:
                n_text = self.font.render(str(n), True, LIGHT_BROWN)
            win.blit(n_text, (i * SQUARE_SIZE, HEIGHT - COORD_FONT_SIZE))

    def draw_pieces(self, win, layout):
        """Draws the Chess game pieces onto the board. Also flips the orientation to match board view."""
        for row in range(ROWS):
            for col in range(COLS):
                piece = layout[row][col]
                if piece is not None:
                    # Transforming the coordinates for player view
                    vrow, vcol = self.virt_coords(row, col)
                    win.blit(pieceImages[piece], (vcol * SQUARE_SIZE + PIECE_OFFSET, vrow * SQUARE_SIZE + PIECE_OFFSET))

    def get_mouse_square(self):
        """Returns the current square that the mouse cursor is located in.
        Also inverts the coordinates depending on board view."""
        mouse_coords = pygame.mouse.get_pos()
        # Transforming the coordinates for player view
        vrow, vcol = self.virt_coords(mouse_coords[1] // SQUARE_SIZE, mouse_coords[0] // SQUARE_SIZE)
        return (vrow, vcol)

    def draw_selected(self, win, moves, engine):
        """Draws highlighted green box for the selected piece and highlighted yellow boxes for valid moves of the
        piece"""
        if self.piece_chosen is not None:
            # Transforming the coordinates for player view
            vrow, vcol = self.virt_coords(*self.piece_chosen)
            if (engine.get_board()[vrow][vcol][0] == 'w' and engine.get_player_turn() == 'White') or \
                    (engine.get_board()[vrow][vcol][0] == 'b' and engine.get_player_turn() == 'Black'):
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                highlight.set_alpha(150)
                highlight.fill(pygame.Color('green'))
                win.blit(highlight, (vcol*SQUARE_SIZE, vrow*SQUARE_SIZE))
                highlight.fill(pygame.Color('yellow'))
                for move in moves:
                    if move.start_row == vrow and move.start_col == vcol:
                        win.blit(highlight, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

    def draw_sidebar(self, win, engine):
        """Draws the sidebar and content"""
        # Drawing background box
        pygame.draw.rect(win, BLACKISH, (WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))

        # Draw turn indicator
        if engine.white_turn:
            text = "White's Turn"
        else:
            text = "Black's Turn"
        n_text = self.font.render(text, True, WHITEISH)
        win.blit(n_text, (WIDTH + 5, 5))

        # Draw captured pieces
        def draw_captures(piece_type, coords):
            count = 0
            for i in engine.pieces_captured:
                if i == piece_type:
                    count += 1
            n_text = self.font.render("{}: {}".format(piece_type[1], count), True, WHITEISH)
            win.blit(n_text, coords)

        n_text = self.font.render("White's Captures", True, WHITEISH)
        win.blit(n_text, (WIDTH + 5, 40))
        draw_captures("bP", (WIDTH + 5, 60))
        draw_captures("bR", (WIDTH + 5, 80))
        draw_captures("bB", (WIDTH + 5, 100))
        draw_captures("bK", (WIDTH + 5, 120))
        draw_captures("bQ", (WIDTH + 5, 140))

        n_text = self.font.render("Blacks's Captures", True, WHITEISH)
        win.blit(n_text, (WIDTH + 5, 160))
        draw_captures("wP", (WIDTH + 5, 180))
        draw_captures("wR", (WIDTH + 5, 200))
        draw_captures("wB", (WIDTH + 5, 220))
        draw_captures("wK", (WIDTH + 5, 240))
        draw_captures("wQ", (WIDTH + 5, 260))
