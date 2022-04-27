import pygame

from constants import *
from board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move

engine = ChessEngine()

FPS = 60

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('Chess')

##### integrating client's socket connection code (Josh)  #####

from server_files.client_network import Network

# buffer to store move data
make_move = None        # this client has made a move to send to opponent
opponent_move = None    # received move made by opponent

def get_player_color(data):
    if connect_message[-1] == '0':
        return WHITE
    else:
        return BLACK

def is_turn():
    if player_color == WHITE and engine.white_turn:
        return True
    if player_color == BLACK and not engine.white_not:
        return True
    return False

n = Network()

# establish connection and receive first
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

        # opponent disconnected. stay ready, waiting for opponent to reconnect
        if reply == OPPONENT_DISCONNECTED:
            payload = READY

        # server is waiting for an opponent to connect
        elif reply == WAITING_FOR_OPPONENT:
            # continue to wait
            payload = WAITING_GAME_START

        # server is waiting for a move
        elif reply == WAITING_FOR_TURN:
            # this client's turn
            if is_turn():
                global make_move
                # no move data to send
                if make_move is None:
                    payload = READY

                # has move data to send
                else:
                    print("SENDING MOVE TO SERVER")
                    # ready move data, empty move data buffer, end turn
                    payload = make_move
                    make_move = None

            # not this client's turn
            else:
                global opponent_move
                # no move data received from opponent
                if opponent_move is None:
                    # stay ready
                    payload = READY

                # received move data from opponent
                else:
                    # store opponent move data into buffer
                    opponent_move = reply
                    opponent_move = None

                    # update game state in game engine and UI
                    print("RECEIVED OPPONENT MOVE FROM SERVER")

                    # start turn, send ready message
                    payload = READY

        net_conn.send(payload)

        print('Sending to server:', payload)
        print('Received from server:', reply)

    except:
        pass

##### end integration code #####

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
                    move = Move(board.selected_piece, mouse_square, engine.board)
                    # call game engine (piece)_move() to get list of valid moves for this piece and location
                    # if move is in valid_moves_list
                        # place move into data buffer shared with client to read and send to server
                        # make_move = move.get_chess_notation()

                        # engine.make_move(move) --- written below
                        # board.selected_piece = None --- written below
                    # else nothing or deselect piece (place piece back)

                    engine.make_move(move)
                    board.selected_piece = None
                else:
                    row, col = mouse_square
                    if not engine.is_empty_square(row, col):
                        board.selected_piece = mouse_square
                        # send row, col, piece to engine.(piece)_move() to get list of valid moves
                        # highlight all the end squares
            # (end indent)
            # else: opponent turn:
                # if opponent move data buffer is not None:
                    # create Move object from opponent move data, need function to convert chess notation to start/end row/col
                    # opponent_move = Move(*startSq*, *endSq*, engine.board)
                    # engine.make_move(opponent_move)

        ##### integration code for sending/receiving data with server (Josh) #####
        communicate_server(n)
        ##### end integration code #####

        board.draw_squares(WIN)
        board.draw_selected(WIN)
        board.draw_pieces(WIN, engine.board)
        pygame.display.update()

    pygame.quit