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

def is_turn():
    if player_color == WHITE and engine.white_turn:
        return True
    if player_color == BLACK and not engine.white_turn:
        return True
    return False

n = Network()

# establish connection and receive first message with this client's color
connect_message = n.connect()

if connect_message == ERROR:
    print(GAME_FULL)
else:
    print(connect_message)
    player_color = get_player_color(connect_message)

    # initial message: waiting for server to indicate game is ready
    message = WAITING_GAME_START
    n.send(message)

def communicate_server(net_conn: Network):
    try:
        reply = net_conn.receive()

        # server sent message (not Move object)
        if isinstance(reply, str):
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
                    # ready payload with move data, empty move data buffer
                    payload = make_move
                    make_move = None

        # received opponent move data
        else:
            global opponent_move
            # store opponent move data into buffer for UI and game engine
            opponent_move = reply
            payload = READY

        net_conn.send(payload)

        print('Sending to server:', payload)
        print('Received from server:', reply)

        return reply

    except:
        pass


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        # get server message regarding game state
        server_state = communicate_server(n)

        mouse_square = board.get_mouse_square()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # game is playing (have opponent and is opponent is connected) and is this client's turn
            if server_state != WAITING_FOR_OPPONENT and server_state != OPPONENT_DISCONNECTED and is_turn():

                # user clicks on the board
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # placing piece on the designated location
                    if board.selected_piece:
                        move = Move(board.selected_piece, mouse_square, engine.board)
                        # call game engine (piece)_move() to get list of valid moves for this piece and location
                        # if move is in valid_moves_list
                            # place move into data buffer shared with client to read and send to server

                            # to be indented with above check
                            # engine.make_move(move) --- written below
                            # board.selected_piece = None --- written below
                            # store Move object into make_move data buffer to send to server -- written below

                        engine.make_move(move)
                        board.selected_piece = None
                        global make_move
                        make_move = move
                        # else:
                            # nothing or deselect piece (place piece back)

                    # selecting piece to move
                    else:
                        row, col = mouse_square
                        if not engine.is_empty_square(row, col):
                            board.selected_piece = mouse_square
                            # send row, col, piece to engine.(piece)_move() to get list of valid moves
                            # highlight all the end squares

            # opponent's turn
            else:
                global opponent_move
                # opponent's move data buffer contains data (Move object)
                if opponent_move is not None:
                    # make the move in the engine and clear the data buffer
                    engine.make_move(opponent_move)
                    opponent_move = None

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit