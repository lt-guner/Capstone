import pygame

from .constants import *
from .board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move

from .client_network import Network

def get_player_color(data):
    """
    Returns a string of the player color.
    Determined by parsing the initial string message upon connecting with the server.
    """
    if data[-1] == '0':
        print('Player Color: White')
        return WHITE
    else:
        print('Player Color: Black')
        return BLACK

def is_turn(color, engine: ChessEngine):
    """
    Returns True if the inputted string color is the turn player in the game engine.
    Otherwise returns False.
    """
    if color == WHITE and engine.white_turn:
        return True
    if color == BLACK and not engine.white_turn:
        return True
    return False

def init_connect(network):
    """
    Returns a string of the player color. Returns None if connection error.
    Initializes a network connection with the server for online multiplayer.
    """
    # establish connection and receive first message with this client's color
    connect_message = network.connect()

    if connect_message == ERROR:
        print(GAME_FULL)
        return None
    else:
        print(connect_message)

        # initial message: waiting for server to indicate game is ready
        message = WAITING_GAME_START
        network.send(message)

        return get_player_color(connect_message)

def communicate_server(net_conn: Network):
    """
    Returns the data received from the server.
    Receives data from the server.
    Determines appropriate response according to UI and engine states.
    Sends the response to the server.
    """
    try:
        reply = net_conn.receive()

        # opponent disconnected. disconnect from server
        if reply == OPPONENT_DISCONNECTED:
            net_conn.close()

        # server is waiting for an opponent to connect
        elif reply == WAITING_FOR_OPPONENT:
            # continue to wait
            payload = WAITING_GAME_START

        # server is waiting for a move
        elif reply == WAITING_FOR_TURN:
            # UI will only store move data into make_move data buffer if user's turn
            global make_move
            # no move data to send
            if make_move is None:
                payload = READY

            # has move data to send
            else:
                print('Sending move to opponent', make_move.get_move_legible())
                # ready payload with move data, empty move data buffer
                payload = make_move
                make_move = None

        # received opponent move data
        else:
            global opponent_move
            print('Received opponent move:', reply.get_move_legible())

            # store opponent move data into buffer for UI and game engine
            opponent_move = reply
            payload = READY

        net_conn.send(payload)

        # print('Sending to server:', payload)
        # print('Received from server:', reply)

        return reply

    except:
        pass

def is_game_over(engine: ChessEngine):
    return engine.checkmate or engine.stalemate

def draw_board(board: Board, engine: ChessEngine):
    """
    Draws the current chess board state and updates the rendered image.
    """
    # Draws the board
    board.draw_squares(WIN)
    board.draw_coords(WIN)
    board.draw_selected(WIN)
    board.draw_pieces(WIN, engine.board)

    if engine.checkmate:
        # draw checkmate text
        pass
    elif engine.stalemate:
        # draw stalemate text
        pass

    pygame.display.update()

def draw_sel_menu(clock):
    """
    Draws the menu for the user to select single player or multiplayer
    """
    while game_state == SEL_MENU:
        clock.tick(FPS)

        render_ai_difficulty = False
        # get mouse coordinates

        for event in pygame.event.get():
            # Allows the user to quit the game when they hit the exit button
            if event.type == pygame.QUIT:
                global run
                run = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # if render_ai_difficulty is False:
                    # if mouse location is for single player:
                        # render_ai_difficulty = True
                    # elif mouse location is for online multiplayer:
                        # global game_state
                        # game_state = ONLINE_PLAY
                        # return
                # else:
                    # if mouse location is for easy difficulty:
                        # global ai_difficulty
                        # ai_difficulty = EAS_DIFF
                        # global game_state
                        # game_state = SINGLE_PLAY
                    # if mouse location is for medium difficulty:
                        # global ai_difficulty:
                        # ai_difficulty = MED_DIFF
                        # global game_state
                        # game_state = SINGLE_PLAY
                    # if mouse location is for hard difficulty:
                        # global ai_difficulty:
                        # ai_difficulty = HAR_DIFF
                        # global game_state
                        # game_state = SINGLE_PLAY

        # draw select menu UI elements
        # if render_ai_difficulty:
            # draw the difficulty options
        # else:
            # draw single player vs AI / online vs player options

        # update display

def play_singleplayer(clock, difficulty):
    """
    Executes a game of chess against a computer AI
    """
    player_color = WHITE  # do we want to implement a color selection? (display after selecting difficulty in draw_sel_menu)
    engine = ChessEngine()
    board = Board(player_color)

    # initialize AI class

    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    global game_state
    while game_state == SINGLE_PLAY:
        clock.tick(FPS)

        # What coordinates the mouse is in
        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            # Allows the user to quit the game when they hit the exit button
            if event.type == pygame.QUIT:
                global run
                run = False
                return

            # game is not over
            if not is_game_over(engine):
                if is_turn(player_color, engine):
                    # user clicks on the board
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # second click: placing a selected piece on the board
                        if board.piece_chosen:
                            move = Move(board.piece_chosen, mouse_square, engine.board)

                            # make a move if it is a valid move and set move_made to true
                            if move in valid_moves:
                                engine.make_move(move)
                                move_made = True

                                # store Move object into data buffer to send to server
                                global make_move
                                make_move = move
                                print('UI/Engine: Storing move to send. END TURN.')
                            board.piece_chosen = None

                        # first click: selecting a piece to move
                        else:
                            row, col = mouse_square
                            # Won't allow a user to click on empty square
                            if not engine.is_empty_square(row, col):
                                board.piece_chosen = mouse_square
                # AI executes turn
                else:
                    # AI makes a move
                    # if difficulty == EAS_DIFF:
                        # AI makes easy move
                    # elif difficulty == MED_DIFF:
                        # AI makes med move
                    # else:
                        # AI makes hard move
                    move_made = True
                    pass

                # get the next set of valid moves and reset move_made
                if move_made:
                    valid_moves = engine.valid_moves()
                    move_made = False

            # game is over, prompt user to return to select menu
            # else:
                # if event.type == pygame.MOUSEBUTTONDOWN:
                    # if mouse coordinates is on "go back to menu" button:
                        # game_state = SEL_MENU

        draw_board(board, engine)
        # if is_game_over(engine):
            # draw game over message on UI
            # draw a "go back to menu" button

def play_multiplayer(clock):
    """
    Executes a game of chess against another player online
    """
    # connect to server and get player color
    n = Network()
    player_color = init_connect(n)
    opponent_connected = True

    # connection error, return to select menu
    if player_color is None:
        global game_state
        game_state = SEL_MENU
        return

    engine = ChessEngine()
    board = Board(player_color)

    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    global game_state
    while game_state == ONLINE_PLAY:
        clock.tick(FPS)

        # get message from server regarding game state
        server_state = communicate_server(n)

        # opponent disconnected, return to select menu
        if server_state == OPPONENT_DISCONNECTED:
            opponent_connected = False

        # What coordinates the mouse is in
        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            # Allows the user to quit the game when they hit the exit button
            if event.type == pygame.QUIT:
                global run
                run = False
                return

            # game is not over
            if not is_game_over(engine): # will exist in ChessEngine
                # server is waiting to receive a Move object, and it's this client's turn
                if server_state == WAITING_FOR_TURN and is_turn(player_color, engine):
                    # user clicks on the board
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # second click: placing a selected piece on the board
                        if board.piece_chosen:
                            move = Move(board.piece_chosen, mouse_square, engine.board)

                            # make a move if it is a valid move and set move_made to true
                            if move in valid_moves:
                                engine.make_move(move)
                                move_made = True

                                # store Move object into data buffer to send to server
                                global make_move
                                make_move = move
                                print('UI/Engine: Storing move to send. END TURN.')
                            board.piece_chosen = None

                        # first click: selecting a piece to move
                        else:
                            row, col = mouse_square
                            # Won't allow a user to click on empty square
                            if not engine.is_empty_square(row, col):
                                board.piece_chosen = mouse_square

                # opponent's turn
                else:
                    global opponent_move
                    # opponent's move data buffer contains data (Move object)
                    if opponent_move is not None:
                        print('UI/Engine: Making opponent move. START TURN.')
                        move_made = True
                        # make the move in the engine and clear the data buffer
                        engine.make_move(opponent_move)
                        opponent_move = None

                # get the next set of valid moves and reset move_made
                if move_made:
                    valid_moves = engine.valid_moves()
                    move_made = False

            # game is over, prompt user to return to select menu
            # else:
                # if event.type == pygame.MOUSEBUTTONDOWN:
                    # if mouse coordinates is on "go back to menu" button:
                        # game_state = SEL_MENU

        draw_board(board, engine)
        # if is_game_over(engine):
            # draw game over message on UI
            # draw a "go back to menu" button
        # elif opponent_connected is False:
            # draw opponent disconnected message on UI
            # draw a "go back to menu" button


# set window parameters and caption name
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(WIN_NAME)

# buffer to store move data
make_move = None        # this client has made a move to send to opponent
opponent_move = None    # received move made by opponent

run = True
game_state = ONLINE_PLAY        # change to SEL_MENU when implemented
ai_difficulty = None

def main():
    clock = pygame.time.Clock()
    pygame.init()   # create the game window

    while run:
        if game_state == SEL_MENU:
            draw_sel_menu(clock)
        elif game_state == SINGLE_PLAY:
            play_singleplayer(clock, ai_difficulty)
        elif game_state == ONLINE_PLAY:
            play_multiplayer(clock)

    pygame.quit