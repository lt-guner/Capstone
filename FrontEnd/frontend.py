import pygame

from .constants import *
from .board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move

from .client_network import Network

engine = ChessEngine()

FPS = 60

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Chess')

# buffer to store move data
make_move = None        # this client has made a move to send to opponent
opponent_move = None    # received move made by opponent

def get_player_color(data):
    if data[-1] == '0':
        return WHITE
    else:
        return BLACK

def is_turn(color):
    if color == WHITE and engine.white_turn:
        return True
    if color == BLACK and not engine.white_turn:
        return True
    return False

def init_connect(network):
    # establish connection and receive first message with this client's color
    connect_message = network.connect()

    if connect_message == ERROR:
        print(GAME_FULL)
    else:
        print(connect_message)

        # initial message: waiting for server to indicate game is ready
        message = WAITING_GAME_START
        network.send(message)

        return get_player_color(connect_message)

def communicate_server(net_conn: Network):
    try:
        reply = net_conn.receive()

        # opponent disconnected. stay ready, waiting for opponent to reconnect
        if reply == OPPONENT_DISCONNECTED:
            payload = READY

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
                print('SENDING MOVE TO OPPONENT')
                print(make_move.get_move_legible())
                # ready payload with move data, empty move data buffer
                payload = make_move
                make_move = None

        # received opponent move data
        else:
            global opponent_move
            print('RECEIVED OPPONENT MOVE')
            print(reply.get_move_legible())

            # store opponent move data into buffer for UI and game engine
            opponent_move = reply
            payload = READY

        net_conn.send(payload)

        # print('Sending to server:', payload)
        # print('Received from server:', reply)

        return reply

    except:
        pass

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    # connect to server and get player color
    n = Network()
    player_color = init_connect(n)

    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    while run:
        clock.tick(FPS)

        # get message from server regarding game state
        server_state = communicate_server(n)

        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # has opponent and opponent is connected and is this client's turn
            if server_state != WAITING_FOR_OPPONENT and server_state != OPPONENT_DISCONNECTED and is_turn(player_color):
                # user clicks on the board
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # second click: placing a selected piece on the board
                    if board.selected_piece:
                        move = Move(board.selected_piece, mouse_square, engine.board)

                        # make a move if it is a valid move and set move_made to true
                        for i in range(len(valid_moves)):   # can we make this if move in valid_moves?
                            if move == valid_moves[i]:
                                engine.make_move(valid_moves[i])
                                move_made = True

                                # store Move object into data buffer to send to server
                                global make_move
                                make_move = move
                        board.selected_piece = None

                    # first click: selecting a piece to move
                    else:
                        row, col = mouse_square
                        if not engine.is_empty_square(row, col):
                            board.selected_piece = mouse_square

            # opponent's turn
            else:
                global opponent_move
                # opponent's move data buffer contains data (Move object)
                if opponent_move is not None:
                    move_made = True
                    # make the move in the engine and clear the data buffer
                    engine.make_move(opponent_move)
                    opponent_move = None

        # get the next set of valid moves and reset move_made
        if move_made:
            valid_moves = engine.valid_moves()
            move_made = False

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit